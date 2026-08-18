from uuid import UUID

from fastapi import APIRouter

from .core.dependencies import BookingServiceDeps
from .model import BookingCreate

router = APIRouter(prefix="/booking", tags=["BOOKING"])


@router.get("")
def get_bookings(service: BookingServiceDeps):
    return service.index()


@router.post("")
def create_booking(booking: BookingCreate, service: BookingServiceDeps):
    return service.create(booking)


@router.patch("/{booking_id}/cancel")
def cancel_booking(booking_id: UUID, service: BookingServiceDeps):
    return service.cancel(booking_id)
