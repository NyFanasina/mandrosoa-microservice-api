from typing import Annotated

from fastapi import APIRouter, Form

from .core.dependencies import ListingServiceDeps
from .models.listing import ListingCreate, ListingUpdate

router = APIRouter(prefix="/listing", tags=["LISTING"])


@router.get("")
def get_listings(service: ListingServiceDeps):
    return service.index()


@router.post("")
def create_listing(listing: Annotated[ListingCreate, Form()], service: ListingServiceDeps):
    return service.store(listing)


@router.get("/{listing_id}")
def show_a_listing(listing_id: str, service: ListingServiceDeps):
    return service.show(listing_id)


@router.put("/{listing_id}")
def update_a_listing(listing_id: str, listing: ListingUpdate, service: ListingServiceDeps):
    return service.update(listing_id, listing)


@router.delete("/{listing_id}")
def delete_a_listing(listing_id: str, service: ListingServiceDeps):
    return service.destroy(listing_id)
