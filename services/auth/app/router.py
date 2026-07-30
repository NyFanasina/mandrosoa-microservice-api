from typing import Annotated

from fastapi import APIRouter, Cookie, Response

from .core.constant import ENV
from .core.dependencies import UserServiceDeps
from .model import UserCreate, UserResponse, UserUpdate
from .schemas import ApiResponse, Credential

auth_router = APIRouter(prefix="/auth", tags=["Authentification"])


@auth_router.post("")
def register_user(user: UserCreate, service: UserServiceDeps):
    return service.register(user)


@auth_router.post("/login")
def login(
    credential: Credential,
    response: Response,
    service: UserServiceDeps,
):
    return service.login(credential, response)


@auth_router.get("/me")
def get_currrent_user(
    auth_service: UserServiceDeps,
    access_token: Annotated[str, Cookie(alias=ENV["COOKIE_NAME"], include_in_schema=False)] = "",
):
    return auth_service.decode_access_token(access_token)


@auth_router.delete("/logout")
def logout(auth_service: UserServiceDeps, response: Response):
    return auth_service.logout(response)


user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("", response_model=ApiResponse[list[UserResponse]])
def get_user_list(service: UserServiceDeps):
    return service.index()


@user_router.post("", response_model=ApiResponse[UserResponse])
def create_user(user: UserCreate, auth_service: UserServiceDeps):
    return auth_service.register(user)


@user_router.get("/{user_id}", response_model=ApiResponse[UserResponse])
def find_user_by_id(user_id: str, service: UserServiceDeps):
    return service.show(user_id)


@user_router.put("/{user_id}", response_model=ApiResponse[UserResponse])
def update_user(user_id: str, user_data: UserUpdate, service: UserServiceDeps):
    return service.update(user_id, user_data)


@user_router.delete("/{user_id}")
def delete_user(user_id: str, service: UserServiceDeps):
    return service.destroy(user_id)


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
