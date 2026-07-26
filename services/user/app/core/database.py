from os import getenv

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from .. import model  # noqa: F401
from ..utils import logger

load_dotenv()

database_url = getenv("DATABASE_URL") or ""
engine = create_engine(database_url)


def init_database():
    try:
        # SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        logger.info("Connection to the database has been established !")
    except Exception as e:
        raise e.with_traceback(None)


def get_session():
    with Session(engine) as session:
        yield session
