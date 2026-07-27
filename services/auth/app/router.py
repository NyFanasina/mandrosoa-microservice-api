from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .core.dependencies import get_auth_service
from .model import CredentialCreate
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentification"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_service_deps = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: auth_service_deps,
):
    credential = CredentialCreate(email=form_data.username, password=form_data.password)
    return auth_service.authenticate(credential)


@router.post("/register")
def register(credential: CredentialCreate, auth_service: auth_service_deps):
    return auth_service.register(credential)


@router.get("/me")
def get_currrent_user(token: Annotated[str, Depends(oauth2_scheme)], auth_service: auth_service_deps):
    return auth_service.decode_access_token(token)
