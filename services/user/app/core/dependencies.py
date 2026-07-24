from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repository import UserRepository
from ..service import UserService
from .database import get_session


def get_user_repository(session: Annotated[Session, Depends(get_session)]):
    return UserRepository(session)


def get_user_service(repository: Annotated[UserRepository, Depends(get_user_repository)]):
    return UserService(repository)
