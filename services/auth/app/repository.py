from sqlmodel import Session, select

from .model import Credential, CredentialCreate


class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, credential: Credential):
        self.session.add(credential)
        self.session.commit()
        self.session.refresh(credential)
        return credential

    def findByEmail(self, credential: CredentialCreate):
        stm = select(Credential).where(Credential.email == credential.email)
        return self.session.exec(stm).one_or_none()
