from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response

from .core.constant import ENV
from .core.dependencies import get_auth_service
from .model import CredentialCreate
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentification"])

auth_service_deps = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/login")
def login(
    credential: CredentialCreate,
    response: Response,
    auth_service: auth_service_deps,
):
    return auth_service.login(credential, response)


@router.post("/register")
def register(credential: CredentialCreate, auth_service: auth_service_deps):
    return auth_service.register(credential)


@router.get("/me")
def get_currrent_user(
    auth_service: auth_service_deps,
    access_token: Annotated[str, Cookie(alias=ENV["COOKIE_NAME"], include_in_schema=False)] = "",
):
    return auth_service.decode_access_token(access_token)


@router.delete("/logout")
def logout(auth_service: auth_service_deps, response: Response):
    return auth_service.logout(response)


# This part use OAuth2PasswordBearer (not used beacause we switch for cookie based auth)

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

# @router.post("/token", include_in_schema=False)
# def request_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     auth_service: auth_service_deps,
# ):
#     credential = CredentialCreate(email=form_data.username, password=form_data.password)
#     return auth_service.authenticate(credential)


# @router.get("/me")
# def get_currrent_user(token: Annotated[str, Depends(oauth2_scheme)], auth_service: auth_service_deps):
#     return auth_service.decode_access_token(token)
