from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient


async def get_http_client():
    async with AsyncClient(follow_redirects=True) as client:
        yield client


ClientHttpDeps = Annotated[AsyncClient, Depends(get_http_client)]
