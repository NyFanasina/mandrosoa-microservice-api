from sqlmodel import Session, SQLModel, create_engine

from ..models import *
from ..utils import logger
from .constant import ENV

database_url = ENV["DATABASE_URL"]
engine = create_engine(database_url)


def init_database():
    try:
        # SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        logger.info("Connection to the database has been established !")
    except Exception as e:
        raise e


def get_session():
    with Session(engine) as session:
        yield session
