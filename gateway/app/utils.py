import logging
from typing import Any

import jwt

from .core.constant import ENV, routing_table
from .core.exceptions import UnAuthorizedException
from .schema import DecodedToken

logger = logging.getLogger("uvicorn")

ALGORITHM = ENV["JWT_ALGORITHM"]
JWT_SECRET_KEY = ENV["JWT_SECRET_KEY"]


def format_response(code: int = 200, data: Any = None, message=""):
    return {"code": code, "data": data, "message": message}


def guess_service_url(pathname: str):
    try:
        mapped = list(filter(lambda item: pathname.startswith(item[0]), routing_table.items()))
        return f"http://{mapped[0][1]}"
    except IndexError:
        logger.exception(f"No service found for {pathname} in routing table")


def decode_access_token(token: str):
    try:
        if not token:
            return None
        return DecodedToken(**jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM]))
    except jwt.ExpiredSignatureError:
        raise UnAuthorizedException("Token expired")
    except jwt.DecodeError:
        raise UnAuthorizedException("Invalid token")


def unit_test_demo():
    return True
