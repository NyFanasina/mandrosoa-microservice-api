from datetime import datetime, timedelta, timezone
from typing import Final

import jwt
from fastapi import Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError

from .core.constant import ENV
from .core.exceptions import AlreadyExistsException, NotFoundException, UnAuthorizedException
from .model import User, UserCreate, UserUpdate
from .repository import AuthRepository
from .schemas import Credential, Token, TokenPayload
from .utils import format_response, hash_password, verify_password


class UserService:
    ALGORITHM: Final = "HS256"

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def index(self):
        return format_response(data=self.repository.all(), message="List of users")

    def register(self, user: UserCreate):
        try:
            password_hash = hash_password(user.password)
            user_with_hash = User(**user.model_dump(exclude={"password"}), password_hash=password_hash)
            created = self.repository.create(user_with_hash).model_dump(exclude={"password_hash"})
            return format_response(201, created, "User registered")
        except IntegrityError:
            raise AlreadyExistsException("Email already exists in the database")

    def show(self, user_id: str):
        user = self.repository.findById(user_id)

        if user is None:
            raise NotFoundException(message="User Not Found")

        return format_response(data=user, message="User found")

    def update(self, user_id: str, user: UserUpdate):
        db_user = self.repository.findById(user_id)

        if db_user is None:
            raise NotFoundException("User Not Found")

        new_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(new_data)
        data = self.repository.update(db_user)
        return format_response(200, data, "User Updated")

    def destroy(self, user_id: str):
        user = self.repository.findById(user_id)

        if user is None:
            raise NotFoundException("User Not Found")

        self.repository.remove(user)
        return format_response(message="User Deleted")

    def login(self, credential: Credential, response: Response):
        token = self.authenticate(credential)
        response.set_cookie(
            key=ENV["COOKIE_NAME"],
            httponly=ENV["HTTPONLY"],
            secure=ENV["SECURE"],
            samesite=ENV["SAMESITE"],
            max_age=ENV["TOKEN_EXPIRE_IN"],
            value=token.access_token,
        )

        return format_response(200, None, "Connection successful")

    def logout(self, response: Response):
        response.delete_cookie(ENV["COOKIE_NAME"])
        return format_response(200, None, "Disconnection successful")

    def authenticate(self, credential: Credential) -> Token:
        db_user = self.repository.findByEmail(credential.email)

        try:
            if db_user is None:
                raise UnAuthorizedException("Invalid email or password")

            matched = verify_password(credential.password, db_user.password_hash)

            if not matched:
                raise UnAuthorizedException("Invalid email or password")

            token_payload = TokenPayload(id_user=str(db_user.id_user), role=db_user.role)
            access_token = self.__create_access_token(token_payload)
        except InvalidTokenError:
            raise UnAuthorizedException("Invalid token")

        return Token(access_token=access_token, token_type="Bearer")

    def decode_access_token(self, token: str):
        try:
            decoded = jwt.decode(token, ENV["SECRET_KEY"], algorithms=[UserService.ALGORITHM])
            return format_response(200, decoded, "Token decoded")
        except ExpiredSignatureError:
            raise UnAuthorizedException("Token expired")
        except jwt.DecodeError:
            raise UnAuthorizedException("Invalid token")

    def __create_access_token(self, payload: TokenPayload):
        payload.expires_in = datetime.now(tz=timezone.utc) + timedelta(seconds=ENV["TOKEN_EXPIRE_IN"])
        return jwt.encode(payload, ENV["SECRET_KEY"], algorithm=UserService.ALGORITHM)
