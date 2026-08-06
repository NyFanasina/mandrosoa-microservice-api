from pydantic import BaseModel

from .models.listing import ListingWithoutPhoto
from .models.photo import Photo


class ApiResponse[T](BaseModel):
    code: int
    data: T
    message: str


class ListingResponse(ListingWithoutPhoto):
    photos: list[Photo]
