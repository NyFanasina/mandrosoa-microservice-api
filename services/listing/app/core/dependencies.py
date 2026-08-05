from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repository import ListingRepository
from ..service import ListingService
from .database import get_session


def get_listing_repository(session: Annotated[Session, Depends(get_session)]):
    return ListingRepository(session)


def get_listing_service(repository: Annotated[ListingRepository, Depends(get_listing_repository)]):
    return ListingService(repository)


ListingServiceDeps = Annotated[ListingService, Depends(get_listing_service)]
