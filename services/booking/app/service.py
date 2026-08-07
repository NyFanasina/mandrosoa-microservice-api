from uuid import UUID

from .core.enums import BookingStatus
from .core.exceptions import AlreadyExistsException, InvalidInputException, NotFoundException
from .model import Booking, BookingCreate
from .repository import BookingRepository
from .utils import format_response


class BookingService:
    def __init__(self, repository: BookingRepository):
        self.repository = repository

    def index(self):
        return format_response(data=self.repository.all(), message="List of bookings")

    def create(self, new_booking: BookingCreate):
        if new_booking.check_in >= new_booking.check_out:
            raise InvalidInputException("Check in date must be before check out date")

        if not self.repository.check_availability(new_booking.check_in, new_booking.check_out):
            raise AlreadyExistsException("Dates are already booked")

        booking = Booking(**new_booking.model_dump())
        db_booking = self.repository.save(booking)
        return format_response(201, db_booking, "Booking created")

    def cancel(self, id_booking: UUID):
        db_booking = self.repository.find_by_id(id_booking)

        if db_booking is None:
            raise NotFoundException("Booking Not Found")

        db_booking.status = BookingStatus.CANCELED

        return format_response(200, self.repository.save(db_booking), "Booking canceled")
