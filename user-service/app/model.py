from sqlalchemy import func
from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseModel(SQLModel):
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})
