from uuid import UUID

from sqlmodel import Field, SQLModel


class AmenityListingLink(SQLModel, table=True):
    id_listing: UUID = Field(primary_key=True, foreign_key="listing.id_listing")
    id_amenity: UUID = Field(primary_key=True, foreign_key="amenity.id_amenity")
