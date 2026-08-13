from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import Field, SQLModel

from .schemas import Role


class UserBase(SQLModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_items=2)
    email: EmailStr = Field(unique=True)
    phone_number: str
    role: Role


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class User(UserBase, table=True):
    id_user: UUID = Field(primary_key=True, default_factory=uuid4)
    password_hash: str
    is_verified: bool = False
    token_verification: str | None = Field(nullable=True)
    created_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )


class UserResponse(UserBase):
    id_user: UUID
    is_verified: bool = False
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
