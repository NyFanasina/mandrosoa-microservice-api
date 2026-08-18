from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ..core.database import get_session
from ..repository import BookingRepository
from ..service import BookingService


def get_booking_repository(session: Annotated[Session, Depends(get_session)]):
    return BookingRepository(session)


def get_booking_service(repository: Annotated[BookingRepository, Depends(get_booking_repository)]):
    return BookingService(repository)


BookingServiceDeps = Annotated[BookingService, Depends(get_booking_service)]
