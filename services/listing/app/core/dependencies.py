from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..repositories import AmenityRepository, ListingRepository, PhotoRepository
from ..services import AmenityService, ListingService, PhotoService
from .database import get_session


def get_amenity_repository(session: Annotated[Session, Depends(get_session)]):
    return AmenityRepository(session)


def get_amenity_service(repository: Annotated[AmenityRepository, Depends(get_amenity_repository)]):
    return AmenityService(repository)


def get_listing_repository(session: Annotated[Session, Depends(get_session)]):
    return ListingRepository(session)


def get_listing_service(
    listing_repository: Annotated[ListingRepository, Depends(get_listing_repository)],
    amenity_repository: Annotated[AmenityRepository, Depends(get_amenity_repository)],
):
    return ListingService(listing_repository, amenity_repository)


def get_photo_repository(session: Annotated[Session, Depends(get_session)]):
    return PhotoRepository(session)


def get_photo_service(repository: Annotated[PhotoRepository, Depends(get_photo_repository)]):
    return PhotoService(repository)


ListingServiceDeps = Annotated[ListingService, Depends(get_listing_service)]
PhotoServiceDeps = Annotated[PhotoService, Depends(get_photo_service)]
AmenityServiceDeps = Annotated[AmenityService, Depends(get_amenity_service)]
