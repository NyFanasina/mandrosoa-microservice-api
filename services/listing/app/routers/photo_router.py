from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, Request, UploadFile

from ..core.dependencies import PhotoServiceDeps

router = APIRouter(prefix="/photos", tags=["PHOTO"])


@router.post("")
def save_a_photo(
    id_listing: Annotated[UUID, Form()],
    upload: UploadFile,
    request: Request,
    photo_service: PhotoServiceDeps,
):
    return photo_service.store(id_listing, upload, hostname=str(request.headers.get("host")))


@router.delete("/{id_photo}")
def delete_a_photo(id_photo: UUID, photo_service: PhotoServiceDeps):
    return photo_service.destroy(id_photo)
