from uuid import UUID

from fastapi import APIRouter, Request

from ..core.dependencies import ListingServiceDeps
from ..core.enums import ListingStatus
from ..models.listing import ListingCreate, ListingUpdate
from ..schemas import ApiResponse, ListingResponse

router = APIRouter(prefix="/listings", tags=["LISTING"])


@router.get("", response_model=ApiResponse[list[ListingResponse]])
def get_listings(request: Request, service: ListingServiceDeps):
    hostname = str(request.base_url).rstrip("/")
    return service.index(hostname)


@router.post("", response_model=ApiResponse[ListingResponse])
def create_listing(listing: ListingCreate, service: ListingServiceDeps):
    return service.store(listing)


@router.get("/filter", response_model=ApiResponse[list[ListingResponse]])
def filter_listings(
    service: ListingServiceDeps,
    request: Request,
    status: ListingStatus | None = None,
    term: str | None = None,
    city: str | None = None,
    address: str | None = None,
):
    hostname = str(request.base_url).rstrip("/")
    return service.filter(hostname=hostname, status=status, term=term, city=city, address=address)


@router.get("/{listing_id}", response_model=ApiResponse[ListingResponse])
def show_a_listing(listing_id: UUID, request: Request, service: ListingServiceDeps):
    hostname = str(request.base_url).rstrip("/")
    return service.show(listing_id, hostname)


@router.put("/{listing_id}")
def update_a_listing(listing_id: UUID, listing: ListingUpdate, service: ListingServiceDeps):
    return service.update(listing_id, listing)


@router.delete("/{listing_id}")
def delete_a_listing(listing_id: UUID, service: ListingServiceDeps):
    return service.destroy(listing_id)
