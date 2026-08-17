from uuid import UUID

from fastapi import APIRouter

from ..core.dependencies import AmenityServiceDeps
from ..models.amenity import AmenityCreate, AmenityUpdate

router = APIRouter(prefix="/amenities", tags=["AMENITY"])


@router.get("")
def get_amenities(service: AmenityServiceDeps):
    return service.index()


@router.post("")
def create_amenity(amenity: AmenityCreate, service: AmenityServiceDeps):
    return service.store(amenity)


@router.get("/{id_amenity}")
def show_amenity(id_amenity: UUID, service: AmenityServiceDeps):
    return service.show(id_amenity)


@router.put("/{id_amenity}")
def update_amenity(id_amenity: UUID, amenity: AmenityUpdate, service: AmenityServiceDeps):
    return service.update(id_amenity, amenity)


@router.delete("/{id_amenity}")
def destroy_amenity(id_amenity: UUID, service: AmenityServiceDeps):
    return service.destroy(id_amenity)
