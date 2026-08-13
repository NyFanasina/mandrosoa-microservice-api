from uuid import UUID

from sqlmodel import Session, col, or_, select

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

    def filter(self, term: str | None = None, city: str | None = None, address: str | None = None):
        term = term or ""
        city = city or ""
        address = address or ""

        stm = select(Listing).where(
            or_(
                col(Listing.title).contains(term),
                col(Listing.description).contains(term),
                col(Listing.city).contains(term),
                col(Listing.address).contains(term),
                col(Listing.city).contains(city),
                col(Listing.address).contains(address),
            )
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
