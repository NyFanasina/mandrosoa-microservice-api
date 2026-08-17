from typing import Annotated

from fastapi import APIRouter, Cookie, Request, Response

from ..core.constant import ENV
from ..core.dependencies import UserServiceDeps
from ..model import UserCreate, UserResponse
from ..schemas import ApiResponse, Credential

auth_router = APIRouter(prefix="/auth", tags=["Authentification"])


@auth_router.post("", response_model=ApiResponse[UserResponse])
def register_user(user: UserCreate, service: UserServiceDeps, request: Request):
    return service.register(user, str(request.base_url))


@auth_router.post("/login")
def login(
    credential: Credential,
    response: Response,
    service: UserServiceDeps,
):
    return service.login(credential, response)


@auth_router.get("/resend-verification-email")
def resend_verification_email(email: str, service: UserServiceDeps, request: Request):
    return service.resend_verification_email(email, str(request.base_url))


@auth_router.get("/verify-email", response_model=ApiResponse[UserResponse])
def verify_email(token: str, service: UserServiceDeps):
    return service.verify_email(token)


@auth_router.get("/me")
def get_currrent_user(
    auth_service: UserServiceDeps,
    access_token: Annotated[str, Cookie(alias=ENV["COOKIE_NAME"], include_in_schema=False)] = "",
):
    return auth_service.who_am_i(access_token)


@auth_router.delete("/logout")
def logout(auth_service: UserServiceDeps, response: Response):
    return auth_service.logout(response)


# This part use OAuth2PasswordBearer (not used beacause we switch for cookie based auth)

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

# @auth_router.post("/token", include_in_schema=False)
# def request_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     auth_service: UserServiceDeps,
# ):
#     credential = CredentialCreate(email=form_data.username, password=form_data.password)
#     return auth_service.authenticate(credential)


# @auth_router.get("/me")
# def get_currrent_user(token: Annotated[str, Depends(oauth2_scheme)], auth_service: UserServiceDeps):
#     return auth_service.decode_access_token(token)
