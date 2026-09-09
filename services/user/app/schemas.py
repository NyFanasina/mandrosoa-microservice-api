from datetime import datetime
from enum import StrEnum
from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ApiResponse[T](BaseModel):
    code: int
    data: T
    message: str


class Role(StrEnum):
    TRAVELER = "traveler"
    HOST = "host"
    ADMIN = "admin"


class TokenData(TypedDict):
    id_user: UUID
    role: Role


class TokenPayload(dict):
    id_user: str
    role: Role
    expires_in: datetime | None = None


class ResetCode(TypedDict):
    id_user: UUID
    reset_code: int
    expires_in: datetime


class PasswordForgottenUpdate(BaseModel):
    new_password: str = Field(min_length=6)
    reset_password_token: str


class Credential(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
