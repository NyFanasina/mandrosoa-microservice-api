from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .app.core.database import init_database
from .app.core.exceptions import BaseHttpException
from .app.router import router

init_database()

app = FastAPI()
app.include_router(router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: BaseHttpException | HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "data": None,
            "message": exc.message if isinstance(exc, BaseHttpException) else "Not authenticated",
        },
    )


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "data": None,
            "message": [f"{err['loc'][-1]} {err['msg']}" for err in exc.errors()],
        },
    )
