from os import getenv
from sqlmodel import create_engine, SQLModel
from . import model  # noqa: F401


def init_database():
    database_url = getenv("DATABASE_URL") or ""

    try:
        engine = create_engine(database_url)
        SQLModel.metadata.create_all(engine)
        print("    Connection to the database has been established")
    except Exception as e:
        raise e
