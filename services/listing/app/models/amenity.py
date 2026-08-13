from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from .amenity_listing_link import AmenityListingLink

if TYPE_CHECKING:
    from .listing import Listing


class AmenityCreate(SQLModel):
    name: str = Field(min_length=3, unique=True)


class Amenity(AmenityCreate, table=True):
    id_amenity: UUID = Field(primary_key=True, default_factory=uuid4)
    listings: list["Listing"] = Relationship(back_populates="amenities", link_model=AmenityListingLink)


class AmenityUpdate(BaseModel):
    name: str | None
