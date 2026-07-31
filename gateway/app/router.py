from fastapi import APIRouter, Request, Response

from .core.dependencies import ClientHttpDeps
from .utils import guess_service_url

router = APIRouter(prefix="/api", tags=["Gateway API"])


@router.get("")
def hello():
    return {"message": "Hello World"}


@router.api_route("{pathname:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user(pathname: str, client: ClientHttpDeps, request: Request, response: Response):
    service = guess_service_url(pathname)
    url = f"{service}{pathname}"

    body = await request.body()
    result = await client.request(
        method=request.method,
        url=url,
        headers=request.headers,
        content=body,
        params=request.query_params,
    )
    json = result.json()

    response.status_code = result.status_code
    print(result.headers.get_list("set-cookie"))

    for cookie_string in result.headers.get_list("set-cookie"):
        response.headers.append("set-cookie", cookie_string)

    return json
