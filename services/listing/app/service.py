from .core.exceptions import NotFoundException
from .models.listing import Listing, ListingCreate, ListingUpdate
from .repository import ListingRepository
from .utils import format_response


class ListingService:
    def __init__(self, repository: ListingRepository):
        self.repository = repository

    def index(self):
        return format_response(data=self.repository.all(), message="List of listings")

    def store(self, new_listing: ListingCreate):
        listing = Listing(**new_listing.model_dump())
        db_listing = self.repository.create(listing)
        return format_response(201, db_listing, "Listing created")

    def show(self, listing_id: str):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        return format_response(200, db_listing, "Listing found")

    def update(self, listing_id: str, listing: ListingUpdate):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        listing_data = listing.model_dump(exclude_unset=True)
        db_listing.sqlmodel_update(listing_data)

        return format_response(200, self.repository.update(db_listing), "Listing updated")

    def destroy(self, listing_id: str):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        self.repository.remove(db_listing)
        return format_response(200, None, "Listing deleted")
