import os
from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from ..core.exceptions import NotFoundException
from ..models.photo import Photo
from ..repositories import PhotoRepository
from ..utils import format_response, generate_url

PHOTO_DIR = "static/photos"


class PhotoService:
    def __init__(self, repository: PhotoRepository):
        self.repository = repository

    def store(self, id_listing: UUID, upload: UploadFile, hostname: str):
        try:
            extension = str(upload.filename).split(".")[-1]
            uri = f"{PHOTO_DIR}/{uuid4()}.{extension}"

            os.makedirs(PHOTO_DIR, exist_ok=True)

            photo = Photo(id_listing=id_listing, uri=uri)
            db_photo = self.repository.save(photo)
            db_photo.uri = generate_url(hostname, db_photo.uri)

            with open(uri, "wb") as f:
                f.write(upload.file.read())

            return format_response(201, db_photo, "Photo created")
        except IntegrityError:
            raise NotFoundException("Listing Not Found")

    def destroy(self, id_photo: UUID):
        db_photo = self.repository.find_by_id(id_photo)

        if not db_photo:
            raise NotFoundException("Photo Not Found")

        self.repository.remove(db_photo)
        os.remove(db_photo.uri)
        return format_response(200, None, "Photo deleted")
