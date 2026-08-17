from pydantic import BaseModel

from .models.amenity import Amenity
from .models.listing import ListingWithoutPhoto
from .models.photo import Photo


class ApiResponse[T](BaseModel):
    code: int
    data: T
    message: str


class ListingResponse(ListingWithoutPhoto):
    photos: list[Photo]
    amenities: list[Amenity]
