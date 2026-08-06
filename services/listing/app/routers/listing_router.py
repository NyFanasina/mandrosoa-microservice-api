from uuid import UUID

from fastapi import APIRouter, Request

from ..core.dependencies import ListingServiceDeps
from ..models.listing import ListingCreate, ListingUpdate
from ..schemas import ApiResponse, ListingResponse

router = APIRouter(prefix="/listing", tags=["LISTING"])


@router.get("", response_model=ApiResponse[list[ListingResponse]])
def get_listings(request: Request, service: ListingServiceDeps):
    return service.index(str(request.headers.get("host")))


@router.post("")
def create_listing(listing: ListingCreate, service: ListingServiceDeps):
    return service.store(listing)


@router.get("/{listing_id}", response_model=ApiResponse[ListingResponse])
def show_a_listing(listing_id: UUID, request: Request, service: ListingServiceDeps):
    return service.show(listing_id, str(request.headers.get("host")))


@router.put("/{listing_id}")
def update_a_listing(listing_id: UUID, listing: ListingUpdate, service: ListingServiceDeps):
    return service.update(listing_id, listing)


@router.delete("/{listing_id}")
def delete_a_listing(listing_id: UUID, service: ListingServiceDeps):
    return service.destroy(listing_id)
