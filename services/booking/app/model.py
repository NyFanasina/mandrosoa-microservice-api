from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Field, SQLModel

from .core.enums import BookingStatus


class BookingCreate(SQLModel):
    id_user: UUID
    id_listing: UUID
    check_in: date
    check_out: date
    status: BookingStatus = Field(default=BookingStatus.PENDING)


class Booking(BookingCreate, table=True):
    id_booking: UUID = Field(primary_key=True, default_factory=uuid4)
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(default=None)


class BookingUpdate(BaseModel):
    check_in: date | None = None
    check_out: date | None = None
    status: BookingStatus = Field(default=BookingStatus.PENDING)
