from datetime import datetime, timedelta, timezone
from typing import Final
from uuid import UUID

import jwt
from brevo import Brevo
from brevo.core.api_error import ApiError
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from fastapi import Response
from jinja2 import Environment, FileSystemLoader
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import IntegrityError

from .core.constant import ENV
from .core.exceptions import AlreadyExistsException, NotFoundException, UnAuthorizedException
from .model import User, UserCreate, UserUpdate
from .repository import AuthRepository
from .schemas import Credential, Token, TokenPayload
from .security import create_access_token, decode_access_token
from .utils import format_response, hash_password, verify_password


class UserService:
    ALGORITHM: Final = "HS256"

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def index(self):
        return format_response(data=self.repository.all(), message="List of users")

    def register(self, user: UserCreate, base_url: str):
        try:
            password_hash = hash_password(user.password)
            token_verification = self.__generate_token_verification(user)

            user_with_hash = User(
                **user.model_dump(exclude={"password"}),
                password_hash=password_hash,
                token_verification=token_verification,
            )

            verification_url = f"{base_url.rstrip('/')}/auth/verify-email?token={token_verification}"

            created = self.repository.create(user_with_hash).model_dump(exclude={"password_hash"})
            self.__send_email_verification(user, verification_url)
            return format_response(201, created, "User registered")
        except IntegrityError:
            raise AlreadyExistsException("Email already exists in the database")

    def show(self, user_id: UUID):
        user = self.repository.find_by_id(user_id)

        if user is None:
            raise NotFoundException(message="User Not Found")

        return format_response(data=user, message="User found")

    def update(self, user_id: UUID, user: UserUpdate):
        db_user = self.repository.find_by_id(user_id)

        if db_user is None:
            raise NotFoundException("User Not Found")

        new_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(new_data)
        data = self.repository.update(db_user)
        return format_response(200, data, "User Updated")

    def destroy(self, user_id: UUID):
        user = self.repository.find_by_id(user_id)

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
        db_user = self.repository.find_by_email(credential.email)

        try:
            if db_user is None:
                raise UnAuthorizedException("Invalid email or password")

            matched = verify_password(credential.password, db_user.password_hash)

            if not matched:
                raise UnAuthorizedException("Invalid email or password")

            token_payload = TokenPayload(id_user=str(db_user.id_user), role=db_user.role)
            access_token = create_access_token(token_payload)
        except InvalidTokenError:
            raise UnAuthorizedException("Invalid token")

        return Token(access_token=access_token, token_type="Bearer")

    def verify_email(self, token: str):
        try:
            decode_access_token(token)
            user = self.repository.find_by_token_verification(token)

            if user is None:
                raise UnAuthorizedException("Invalid token")

            user.is_verified = True
            verified = self.repository.update(user)

            return format_response(200, verified, "User verified")
        except jwt.DecodeError:
            raise UnAuthorizedException("Invalid token")

    def who_am_i(self, id_user: UUID):
        user = self.repository.find_by_id(id_user)
        return format_response(200, user, "Token decoded")

    def __generate_token_verification(self, user: UserCreate | User):
        payload = {
            "role": user.role,
            "expires_in": str(datetime.now(tz=timezone.utc) + timedelta(seconds=3600)),
        }
        return jwt.encode(payload, ENV["SECRET_KEY"], algorithm=UserService.ALGORITHM)

    def resend_verification_email(self, email: str, base_url: str):
        db_user = self.repository.find_by_email(email)

        if db_user is None:
            raise NotFoundException("User Not Found")

        token_verification = self.__generate_token_verification(db_user)
        verification_url = f"{base_url.rstrip('/')}/auth/verify-email?token={token_verification}"

        db_user.token_verification = token_verification
        self.repository.update(db_user)
        self.__send_email_verification(db_user, verification_url)
        return format_response(200, None, "Email resent")

    def __send_email_verification(self, user: UserCreate | User, verification_url: str):
        full_name = f"{user.first_name} {user.last_name}"
        client = Brevo(api_key=ENV["BREVO_API_KEY"])

        env = Environment(loader=FileSystemLoader("app/email/templates"))
        template = env.get_template("verify_email.html")

        try:
            result = client.transactional_emails.send_transac_email(
                subject="Confirmez votre adresse email - Bienvenue sur Mandrosoa",
                html_content=template.render(recipient_name=full_name, verification_url=verification_url),
                sender=SendTransacEmailRequestSender(
                    name=ENV["BREVO_SENDER_NAME"],
                    email=ENV["BREVO_SENDER_EMAIL"],
                ),
                to=[
                    SendTransacEmailRequestToItem(
                        email=user.email,
                        name=user.first_name,
                    )
                ],
            )

            print("Email sent. Message ID:", result.message_id)
        except ApiError as e:
            print(e.status_code)
            print(e.body)
