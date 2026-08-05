from sqlmodel import Session, select

from .models.listing import Listing


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

    def find_by_id(self, listing_id: str):
        return self.session.get(Listing, listing_id)

    def update(self, listing: Listing):
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(listing)
        return listing

    def remove(self, listing: Listing):
        self.session.delete(listing)
        self.session.commit()
