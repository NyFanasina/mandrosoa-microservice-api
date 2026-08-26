from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlmodel import Session

from ..core.exceptions import ForbiddenException, UnAuthorizedException
from ..repositories import AmenityRepository, ListingRepository, PhotoRepository
from ..schemas import DecodedToken
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

# ------------------ Guards ------------------

auth_scheme = APIKeyHeader(name="X-User")


def get_current_user(current_user_str: Annotated[str, Depends(auth_scheme)]):
    current_user = DecodedToken.model_validate_json(current_user_str)
    if not current_user:
        raise UnAuthorizedException("Not authenticated")
    return current_user


def get_host_user(current_user: Annotated[DecodedToken, Depends(get_current_user)]):
    if current_user.role not in ["host", "admin"]:
        raise ForbiddenException("Permission denied")
    return current_user


def get_admin_user(current_user: Annotated[DecodedToken, Depends(get_current_user)]):
    if current_user.role != "admin":
        raise ForbiddenException("Permission denied: Only admin can access this route")
    return current_user


UserGuardDeps = Annotated[DecodedToken, Depends(get_current_user)]
HostGuardDeps = Annotated[DecodedToken, Depends(get_host_user)]
AdminGuardDeps = Annotated[DecodedToken, Depends(get_admin_user)]
