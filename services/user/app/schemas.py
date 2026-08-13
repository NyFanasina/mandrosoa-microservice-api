from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class ApiResponse[T](BaseModel):
    code: int
    data: T
    message: str


class Role(StrEnum):
    TRAVELER = "traveler"
    HOST = "host"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(dict):
    id_user: str
    role: Role
    expires_in: datetime | None = None


class Credential(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
