from fastapi import APIRouter, Request, Response

from .core.constant import ENV
from .core.dependencies import ClientHttpDeps
from .utils import decode_access_token, format_response, guess_service_url

router = APIRouter(prefix="/api", tags=["Gateway API"])


@router.get("")
def hello():
    return {"message": "Hello World"}


@router.api_route("{pathname:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user(pathname: str, client: ClientHttpDeps, request: Request, response: Response):
    try:
        headers = request.headers.mutablecopy()
        headers.__delitem__("host")

        decoded_token = decode_access_token(request.cookies.get(ENV["COOKIE_NAME"]) or "")
        # b64_bytes = base64.b64encode(json_str.encode("utf-8"))

        if decoded_token:
            decoded_json = decoded_token.model_dump_json()
            headers.setdefault("X-User", decoded_json)

        service = guess_service_url(pathname)
        url = f"{service}{pathname}"
        body = await request.body()

        result = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
        )

        response.status_code = result.status_code

        for cookie_string in result.headers.get_list("set-cookie"):
            response.headers.append("set-cookie", cookie_string)

        return result.json()
    except Exception as e:
        print(e)
        response.status_code = 500
        return format_response(code=500, message="Internal Server Error")
