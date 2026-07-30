import logging
from typing import Any

from pwdlib import PasswordHash

logger = logging.getLogger("uvicorn")
password_hasher = PasswordHash.recommended()


def format_response(code: int = 200, data: Any = None, message=""):
    return {
        "code": code,
        "data": data,
        "message": message,
    }


def hash_password(password: str):
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hasher.verify(password, hashed_password)
