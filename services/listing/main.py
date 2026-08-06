from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic_core import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .app.core.constant import ENV  # noqa: F401
from .app.core.database import init_database
from .app.core.exceptions import BaseHttpException
from .app.routers import listing_router, photo_router

init_database()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(listing_router)
app.include_router(photo_router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: BaseHttpException | HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "data": None,
            "message": exc.message if isinstance(exc, BaseHttpException) else exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception_handler(request, exc: RequestValidationError):
    print()
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "data": None,
            "message": [f"{err['loc'][-1]} {err['msg']}" for err in exc.errors()],
        },
    )


@app.exception_handler(ValidationError)
async def custom_validation_exception_handler(request, exc: ValidationError):
    print()
    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "data": None,
            "message": [f"{err['loc'][-1]} {err['msg']}" for err in exc.errors()],
        },
    )
