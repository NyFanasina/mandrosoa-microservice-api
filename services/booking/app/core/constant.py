from os import getenv

from dotenv import load_dotenv

loaded = load_dotenv()

if not loaded:
    raise Exception("Please create a .env file")

ENV = {
    "DATABASE_URL": str(getenv("DATABASE_URL")),
}
