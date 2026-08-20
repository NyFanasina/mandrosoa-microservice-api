from uuid import UUID

from fastapi import APIRouter, Request, Response
from pydantic import EmailStr

from ..core.dependencies import UserServiceDeps
from ..model import UserCreate, UserResponse
from ..schemas import ApiResponse, Credential, PasswordForgottenUpdate
from ..security import UserGuardDeps

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


@auth_router.post("/forgotten-password")
def ask_reset_password_code(email: EmailStr, service: UserServiceDeps):
    return service.get_reset_code_by_email(email)


@auth_router.patch("/forgotten-password")
def update_password(password_reset_data: PasswordForgottenUpdate, service: UserServiceDeps):
    return service.update_password(password_reset_data)


@auth_router.get("/forgotten-password/check")
def get_password_reset_token(email: EmailStr, code: int, service: UserServiceDeps):
    return service.check_reset_code(email, code)


@auth_router.get("/resend-verification-email")
def resend_verification_email(email: EmailStr, service: UserServiceDeps, request: Request):
    return service.resend_verification_email(email, str(request.base_url))


@auth_router.get("/verify-email", response_model=ApiResponse[UserResponse])
def verify_email(token: str, service: UserServiceDeps):
    return service.verify_email(token)


@auth_router.get("/me", response_model=ApiResponse[UserResponse])
def who_am_i(service: UserServiceDeps, curent_user: UserGuardDeps):
    return service.who_am_i(UUID(curent_user.get("id_user")))


@auth_router.delete("/logout")
def logout(auth_service: UserServiceDeps, response: Response, _: UserGuardDeps):
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
