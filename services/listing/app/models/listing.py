from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Field, SQLModel

from ..schemas import ListingStatus


class ListingCreate(SQLModel):
    host_id: UUID
    title: str
    description: str
    city: str
    address: str

    bedrooms: int | None = Field(default=None)
    max_guests: int | None = Field(default=None)

    base_price: Decimal = Field(default=0, max_digits=9, decimal_places=2)

    status: ListingStatus = Field(default=ListingStatus.DRAFT)


class Listing(ListingCreate, table=True):
    id_listing: UUID = Field(primary_key=True, default_factory=uuid4)

    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
    published_at: datetime | None = Field(default=None)


class ListingUpdate(BaseModel):
    title: None | str = None
    description: None | str = None
    city: None | str = None
    address: None | str = None
    bedrooms: int | None = None
    max_guests: int | None = None
    base_price: Decimal | None = None
    status: ListingStatus | None = None
