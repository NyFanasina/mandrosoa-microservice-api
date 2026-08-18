from uuid import UUID

from sqlmodel import Session, select

from .model import User


class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def all(self):
        stm = select(User)
        result = self.session.exec(stm).all()
        return result

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_email(self, email: str):
        stm = select(User).where(User.email == email)
        return self.session.exec(stm).one_or_none()

    def find_by_id(self, user_id: UUID):
        return self.session.get(User, user_id)

    def find_by_token_verification(self, token: str):
        stm = select(User).where(User.token_verification == token)
        return self.session.exec(stm).one_or_none()

    def update(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def remove(self, user: User):
        self.session.delete(user)
        self.session.commit()
