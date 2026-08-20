import logging
from typing import Any

logger = logging.getLogger("uvicorn")


def format_response(code: int = 200, data: Any = None, message=""):
    return {"code": code, "data": data, "message": message}


def unit_test_demo():
    return True
