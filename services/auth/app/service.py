from datetime import datetime, timedelta, timezone
from typing import Final

import jwt
from fastapi import Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError

from .core.constants import ENV
from .core.exceptions import AlreadyExistsException, UnAuthorizedException
from .model import Credential, CredentialCreate, Token
from .repository import AuthRepository
from .utils import format_response, hash_password, verify_password


class AuthService:
    ALGORITHM: Final = "HS256"

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register(self, credential: CredentialCreate):
        try:
            hash = hash_password(credential.password)
            db_credential = Credential(email=credential.email, password_hash=hash)
            created = self.repository.create(db_credential).model_dump(exclude={"password_hash"})
            return format_response(201, created, "Credential registered")
        except IntegrityError:
            raise AlreadyExistsException("Email already exists in the database")

    def login(self, credential: CredentialCreate, response: Response):
        token = self.authenticate(credential)
        response.set_cookie(
            key=ENV["COOKIE_NAME"],
            value=token.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ENV["TOKEN_EXPIRE_IN"],
        )

        return format_response(200, None, "Connection successful")

    def logout(self, response: Response):
        response.delete_cookie(ENV["COOKIE_NAME"])
        return format_response(200, None, "Disconnection successful")

    def authenticate(self, credential: CredentialCreate) -> Token:
        db_credentials = self.repository.findByEmail(credential)

        try:
            if db_credentials is None:
                raise UnAuthorizedException("Invalid email or password")

            matched = verify_password(credential.password, db_credentials.password_hash)

            if not matched:
                raise UnAuthorizedException("Invalid email or password")

            access_token = self.__create_access_token(db_credentials)
        except InvalidTokenError:
            raise UnAuthorizedException("Invalid token")

        return Token(access_token=access_token, token_type="Bearer")

    def decode_access_token(self, token: str):
        try:
            decoded = jwt.decode(token, ENV["SECRET_KEY"], algorithms=[AuthService.ALGORITHM])
            return format_response(200, decoded, "Token decoded")
        except ExpiredSignatureError:
            raise UnAuthorizedException("Token expired")
        except jwt.DecodeError:
            raise UnAuthorizedException("Invalid token")

    def __create_access_token(self, credential: Credential):
        to_encode = credential.model_dump(exclude={"id_user", "password_hash"})
        to_encode["id_user"] = str(credential.id_user)
        expire_in = datetime.now(tz=timezone.utc) + timedelta(seconds=ENV["TOKEN_EXPIRE_IN"])
        to_encode.update({"exp": expire_in})

        return jwt.encode(to_encode, ENV["SECRET_KEY"], algorithm=AuthService.ALGORITHM)
