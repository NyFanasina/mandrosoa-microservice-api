from uuid import UUID

from sqlmodel import Session, col, func, or_, select, true

from ..core.enums import ListingStatus
from ..models.listing import Listing


class ListingRepository:
    def __init__(self, session: Session):
        self.session = session

    def all(self):
        stm = select(Listing)
        result = self.session.exec(stm).all()
        return result

    def create(self, listing: Listing):
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(listing)
        return listing

    def find_by_id(self, listing_id: UUID):
        return self.session.get(Listing, listing_id)

    def filter(
        self,
        status: ListingStatus | None = None,
        term: str | None = None,
        city: str | None = None,
        address: str | None = None,
    ):

        term = (term or "").lower()
        city = (city or "").lower()
        address = (address or "").lower()

        stm = select(Listing).where(
            Listing.status == status if status else true(),
            func.lower(Listing.city).contains(func.lower(city)),
            func.lower(Listing.address).contains(address),
            or_(
                func.lower(col(Listing.title)).contains(term),
                func.lower(col(Listing.description)).contains(term),
                func.lower(col(Listing.city)).contains(term),
                func.lower(col(Listing.address)).contains(term),
            ),
        )
        return self.session.exec(stm).all()

    def update(self, listing: Listing):
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(listing)
        return listing

    def remove(self, listing: Listing):
        self.session.delete(listing)
        self.session.commit()
