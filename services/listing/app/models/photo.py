from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from ..models.listing import Listing


class Photo(SQLModel, table=True):
    id_photo: UUID = Field(primary_key=True, default_factory=uuid4)
    id_listing: UUID = Field(foreign_key="listing.id_listing")
    uri: str
    listing: Listing | None = Relationship(back_populates="photos")
