from enum import StrEnum

from pydantic import BaseModel


class Role(StrEnum):
    TRAVELER = "traveler"
    HOST = "host"
    ADMIN = "admin"


class DecodedToken(BaseModel):
    id_user: str
    role: Role
