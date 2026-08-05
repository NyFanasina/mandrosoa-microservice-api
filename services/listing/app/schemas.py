from enum import StrEnum

from pydantic import BaseModel


class ApiResponse[T](BaseModel):
    code: int
    data: T
    message: str


class ListingStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
