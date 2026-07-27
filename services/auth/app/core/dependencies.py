from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repository import AuthRepository
from ..service import AuthService
from .database import get_session


def get_auth_repository(session: Annotated[Session, Depends(get_session)]):
    return AuthRepository(session)


def get_auth_service(repository: Annotated[AuthRepository, Depends(get_auth_repository)]):
    return AuthService(repository)
