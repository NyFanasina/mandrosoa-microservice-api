import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class Role(StrEnum):
    TRAVELER = "traveler"
    HOST = "host"
    ADMIN = "admin"


class UserCreate(SQLModel):
    user_id: uuid.UUID | None = Field(primary_key=True)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_items=2)
    role: Role
    phone_number: str
    is_verified: bool = False


class User(UserCreate, table=True):
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    role: Role | None = None
    phone_number: str | None = None
    is_verified: bool | None = None
