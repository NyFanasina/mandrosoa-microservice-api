from datetime import datetime, timedelta, timezone
from typing import Annotated, cast
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import APIKeyCookie
from jwt.exceptions import ExpiredSignatureError

from .core.constant import ENV
from .core.exceptions import ForbiddenException, UnAuthorizedException
from .model import User, UserCreate
from .schemas import ResetCode, TokenPayload

ALGORITHM = ENV["JWT_ALGORITHM"]
JWT_SECRET_KEY = ENV["SECRET_KEY"]


def decode_access_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise UnAuthorizedException("Token expired")
    except jwt.DecodeError:
        raise UnAuthorizedException("Invalid token")


def decode_reset_code_token(token: str) -> ResetCode:
    try:
        return cast(ResetCode, jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM]))
    except ExpiredSignatureError:
        raise UnAuthorizedException("Token expired")
    except jwt.DecodeError:
        raise UnAuthorizedException("Invalid token")


def create_access_token(payload: TokenPayload, exp: int | None = None):
    payload.expires_in = datetime.now(tz=timezone.utc) + timedelta(seconds=exp or ENV["TOKEN_EXPIRE_IN"])
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def generate_password_reset_token(id_user: UUID, reset_code: int):
    payload = {
        "id_user": str(id_user),
        "reset_code": reset_code,
        "expires_in": str(datetime.now(tz=timezone.utc) + timedelta(seconds=3600)),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def generate_token_verification(user: UserCreate | User):
    payload = {
        "role": user.role,
        "expires_in": str(datetime.now(tz=timezone.utc) + timedelta(seconds=3600)),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


# ------------------ Guards ------------------
cookie_scheme = APIKeyCookie(name=ENV["COOKIE_NAME"])


def get_currrent_user(access_token: Annotated[str, Depends(cookie_scheme)]):
    return decode_access_token(access_token)


def get_admin_user(current_user: Annotated[dict, Depends(get_currrent_user)]):
    if current_user.get("role") != "admin":
        raise ForbiddenException("Only admin can access this route")

    return current_user


AdminGuardDeps = Annotated[dict, Depends(get_admin_user)]
UserGuardDeps = Annotated[dict, Depends(get_currrent_user)]
