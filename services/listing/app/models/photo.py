from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Photo(SQLModel, table=True):
    id_photo: UUID = Field(primary_key=True, default_factory=uuid4)
    listing_id: UUID = Field(foreign_key="listing.id_listing")
    uri: str
