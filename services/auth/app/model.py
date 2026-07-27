from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class CredentialCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=6)


class Credential(SQLModel, table=True):
    id_user: UUID = Field(primary_key=True, default_factory=uuid4)
    email: EmailStr = Field(unique=True)
    password_hash: str
