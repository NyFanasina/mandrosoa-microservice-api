from sqlmodel import Session, select

from ..models.amenity import Amenity


class AmenityRepository:
    def __init__(self, session: Session):
        self.session = session

    def all(self):
        return self.session.exec(select(Amenity)).all()

    def create(self, amenity: Amenity):
        self.session.add(amenity)
        self.session.commit()
        self.session.refresh(amenity)
        return amenity

    def find_by_id(self, id_amenity: str):
        return self.session.get(Amenity, id_amenity)

    def update(self, amenity: Amenity):
        self.session.add(amenity)
        self.session.commit()
        self.session.refresh(amenity)
        return amenity

    def remove(self, amenity: Amenity):
        self.session.delete(amenity)
        self.session.commit()
