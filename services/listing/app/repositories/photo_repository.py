from uuid import UUID

from sqlmodel import Session

from ..models import Photo


class PhotoRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, Photo: Photo):
        self.session.add(Photo)
        self.session.commit()
        self.session.refresh(Photo)
        return Photo

    def find_by_id(self, id_photo: UUID):
        return self.session.get(Photo, id_photo)

    def remove(self, Photo: Photo):
        self.session.delete(Photo)
        self.session.commit()
