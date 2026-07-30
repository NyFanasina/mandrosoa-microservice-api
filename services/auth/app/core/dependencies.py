from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repository import AuthRepository
from ..service import UserService
from .database import get_session


def get_auth_repository(session: Annotated[Session, Depends(get_session)]):
    return AuthRepository(session)


def get_auth_service(repository: Annotated[AuthRepository, Depends(get_auth_repository)]):
    return UserService(repository)


UserServiceDeps = Annotated[UserService, Depends(get_auth_service)]
