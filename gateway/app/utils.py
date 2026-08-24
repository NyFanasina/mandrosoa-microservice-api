import logging
from typing import Any

from .core.constant import routing_table

logger = logging.getLogger("uvicorn")


def format_response(code: int = 200, data: Any = None, message=""):
    return {"code": code, "data": data, "message": message}


def guess_service_url(pathname: str):
    try:
        mapped = list(filter(lambda item: pathname.startswith(item[0]), routing_table.items()))
        return f"http://{mapped[0][1]}"
    except IndexError:
        logger.exception(f"No service found for {pathname} in routing table")


def unit_test_demo():
    return True
