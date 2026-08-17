from datetime import date
from uuid import UUID

from sqlmodel import Session, and_, or_, select

from .model import Booking


class BookingRepository:
    def __init__(self, session: Session):
        self.session = session

    def all(self):
        stm = select(Booking)
        return self.session.exec(stm).all()

    def save(self, booking: Booking):
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking

    def find_by_id(self, id_booking: UUID):
        return self.session.get(Booking, id_booking)

    def check_availability(self, check_in: date, check_out: date):
        stm = select(Booking).where(
            or_(
                or_(
                    and_(
                        Booking.check_in <= check_in,
                        check_in < Booking.check_out,
                    ),
                    and_(
                        Booking.check_in < check_out,
                        check_out < Booking.check_out,
                    ),
                ),
                or_(
                    and_(
                        check_in <= Booking.check_in,
                        Booking.check_in < check_out,
                    ),
                    and_(
                        check_in < Booking.check_out,
                        Booking.check_out < check_out,
                    ),
                ),
            )
        )
        print(self.session.exec(stm).first())
        return not self.session.exec(stm).first()
