from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, Request, UploadFile

from ..core.dependencies import HostGuardDeps, PhotoServiceDeps

router = APIRouter(prefix="/listings/photos", tags=["PHOTO"])


@router.post("")
def save_a_photo(
    id_listing: Annotated[UUID, Form()],
    upload: UploadFile,
    request: Request,
    photo_service: PhotoServiceDeps,
    _: HostGuardDeps,
):
    hostname = str(request.base_url).rstrip("/")
    return photo_service.store(id_listing, upload, hostname=hostname)


@router.delete("/{id_photo}")
def delete_a_photo(id_photo: UUID, photo_service: PhotoServiceDeps, _: HostGuardDeps):
    return photo_service.destroy(id_photo)
