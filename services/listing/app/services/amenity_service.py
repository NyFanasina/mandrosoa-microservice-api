from ..core.exceptions import NotFoundException
from ..models.amenity import Amenity, AmenityCreate, AmenityUpdate
from ..repositories.amenity_repository import AmenityRepository
from ..utils import format_response


class AmenityService:
    def __init__(self, repository: AmenityRepository):
        self.repository = repository

    def index(self):
        amenities = self.repository.all()
        return format_response(200, amenities, "Amenity list")

    def store(self, new_amenity: AmenityCreate):
        amenity = Amenity(name=new_amenity.name)
        created = self.repository.create(amenity)
        return format_response(201, created, "Amenity created")

    def show(self, id_amenity):
        amenity = self.repository.find_by_id(id_amenity)
        return format_response(200, amenity, "Amenity found")

    def update(self, id_amenity, amenity: AmenityUpdate):
        db_amenity = self.repository.find_by_id(id_amenity)

        if not db_amenity:
            raise NotFoundException("Amenity Not Found")

        amenity_values = amenity.model_dump(exclude_unset=True)
        db_amenity.sqlmodel_update(amenity_values)
        updated = self.repository.update(db_amenity)
        return format_response(200, updated, "Amenity updated")

    def destroy(self, id_amenity):
        amenity = self.repository.find_by_id(id_amenity)

        if not amenity:
            raise NotFoundException

        self.repository.remove(amenity)
        return format_response(200, None, "Amenity deleted")
