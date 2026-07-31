import logging
from typing import Any

from .core.constant import routing_table

logger = logging.getLogger("uvicorn")


def format_response(code: int = 200, data: Any = None, message=""):
    return {"code": code, "data": data, "message": message}


def guess_service_url(pathname: str):
    mapped = list(filter(lambda item: pathname.startswith(item[0]), routing_table.items()))
    return f"http://{mapped[0][1]}"
