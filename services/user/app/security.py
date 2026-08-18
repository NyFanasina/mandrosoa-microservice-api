from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import APIKeyCookie
from jwt.exceptions import ExpiredSignatureError

from .core.constant import ENV
from .core.exceptions import ForbiddenException, UnAuthorizedException
from .schemas import TokenPayload

ALGORITHM = ENV["JWT_ALGORITHM"]


def decode_access_token(token: str):
    try:
        return jwt.decode(token, ENV["SECRET_KEY"], algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise UnAuthorizedException("Token expired")
    except jwt.DecodeError:
        raise UnAuthorizedException("Invalid token")


def create_access_token(payload: TokenPayload, exp: int | None = None):
    payload.expires_in = datetime.now(tz=timezone.utc) + timedelta(seconds=exp or ENV["TOKEN_EXPIRE_IN"])
    return jwt.encode(payload, ENV["SECRET_KEY"], algorithm=ALGORITHM)


cookie_scheme = APIKeyCookie(name=ENV["COOKIE_NAME"])


def get_currrent_user(access_token: Annotated[str, Depends(cookie_scheme)]):
    return decode_access_token(access_token)


def get_admin_user(current_user: Annotated[dict, Depends(get_currrent_user)]):
    if current_user.get("role") != "admin":
        raise ForbiddenException("Only admin can access this route")

    return current_user


AdminGuardDeps = Annotated[dict, Depends(get_admin_user)]
UserGuardDeps = Annotated[dict, Depends(get_currrent_user)]
