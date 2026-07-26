from collections.abc import Sequence

from sqlmodel import Session, select

from .model import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> Sequence[User]:
        stm = select(User)
        result = self.session.exec(stm)
        return result.all()

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def findById(self, user_id: str):
        stm = select(User).where(User.user_id == user_id)
        return self.session.exec(stm).one_or_none()

    def update(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def remove(self, user: User):
        self.session.delete(user)
        self.session.commit()
