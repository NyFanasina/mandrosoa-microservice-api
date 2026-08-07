import os
from collections.abc import Sequence
from uuid import UUID

from ..core.exceptions import NotFoundException
from ..models.listing import Listing, ListingCreate, ListingUpdate
from ..repositories.listing_repository import ListingRepository
from ..utils import format_response, generate_url


class ListingService:
    def __init__(self, repository: ListingRepository):
        self.repository = repository

    def index(self, hostname: str):
        listings = self.repository.all()
        listings = self.__generate_url_for_photo(hostname, listings)

        return format_response(data=listings, message="List of listings")

    def store(self, new_listing: ListingCreate):
        listing = Listing(**new_listing.model_dump())
        db_listing = self.repository.create(listing)
        return format_response(201, db_listing, "Listing created")

    def show(self, listing_id: UUID, hostname: str):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        db_listing = self.__generate_url_for_photo(hostname, db_listing)

        return format_response(200, db_listing, "Listing found")

    def filter(self, hostname: str, term: str | None, city: str | None, address: str | None):
        listings = self.repository.filter(term=term, city=city, address=address)
        listings = self.__generate_url_for_photo(hostname, listings)
        return format_response(data=listings, message="Listing matching term")

    def update(self, listing_id: UUID, listing: ListingUpdate):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        listing_data = listing.model_dump(exclude_unset=True)
        db_listing.sqlmodel_update(listing_data)

        return format_response(200, self.repository.update(db_listing), "Listing updated")

    def destroy(self, listing_id: UUID):
        db_listing = self.repository.find_by_id(listing_id)

        if db_listing is None:
            raise NotFoundException("Listing Not Found")

        self.repository.remove(db_listing)

        for photo in db_listing.photos:
            os.remove(photo.uri)

        return format_response(200, None, "Listing deleted")

    def __generate_url_for_photo(self, hostname: str, listings: Sequence[Listing] | Listing | None):
        if listings is None:
            return []
        next_listings = [listings] if isinstance(listings, Listing) else listings

        for listing in next_listings:
            for photo in listing.photos:
                photo.uri = generate_url(hostname, photo.uri)

        if isinstance(listings, Listing):
            return next_listings[0]

        return next_listings
