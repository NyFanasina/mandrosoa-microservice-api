from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repositories import PhotoRepository
from ..repositories.listing_repository import ListingRepository
from ..services import ListingService, PhotoService
from .database import get_session


def get_listing_repository(session: Annotated[Session, Depends(get_session)]):
    return ListingRepository(session)


def get_listing_service(repository: Annotated[ListingRepository, Depends(get_listing_repository)]):
    return ListingService(repository)


def get_photo_repository(session: Annotated[Session, Depends(get_session)]):
    return PhotoRepository(session)


def get_photo_service(repository: Annotated[PhotoRepository, Depends(get_photo_repository)]):
    return PhotoService(repository)


ListingServiceDeps = Annotated[ListingService, Depends(get_listing_service)]
PhotoServiceDeps = Annotated[PhotoService, Depends(get_photo_service)]
