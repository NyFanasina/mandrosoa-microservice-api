from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel

from ..core.enums import ListingStatus
from .amenity_listing_link import AmenityListingLink

if TYPE_CHECKING:
    from ..models import Amenity, Photo


class ListingBase(SQLModel):
    title: str
    description: str
    city: str
    address: str
    bedrooms: int | None = Field(default=None)
    max_guests: int | None = Field(default=None)
    base_price: Decimal = Field(default=0, max_digits=9, decimal_places=2)
    status: ListingStatus = Field(default=ListingStatus.DRAFT)


class ListingInputCreate(ListingBase):  # Schema for swagger
    amenity_ids: list[UUID] = []


class ListingCreate(ListingInputCreate):
    id_host: UUID


class ListingWithoutPhoto(ListingBase):
    id_listing: UUID = Field(primary_key=True, default_factory=uuid4)
    id_host: UUID
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(default=None)
    published_at: datetime | None = Field(default=None)


class Listing(ListingWithoutPhoto, table=True):
    photos: list["Photo"] = Relationship(back_populates="listing", cascade_delete=True)
    amenities: list["Amenity"] = Relationship(back_populates="listings", link_model=AmenityListingLink)


class ListingUpdate(BaseModel):
    title: None | str = None
    description: None | str = None
    city: None | str = None
    address: None | str = None
    bedrooms: int | None = None
    max_guests: int | None = None
    base_price: Decimal | None = None
    status: ListingStatus | None = None
