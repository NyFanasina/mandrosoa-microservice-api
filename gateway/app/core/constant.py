from os import getenv
from typing import TypedDict

from dotenv import load_dotenv


class Env(TypedDict):
    COOKIE_NAME: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    USER_SERVICE_URL: str
    LISTING_SERVICE_URL: str


loaded = load_dotenv()

if not loaded:
    raise Exception("Please create a .env file")


ENV: Env = {
    "COOKIE_NAME": getenv("COOKIE_NAME", ""),
    "JWT_ALGORITHM": getenv("JWT_ALGORITHM", ""),
    "JWT_SECRET_KEY": getenv("JWT_SECRET_KEY", ""),
    "USER_SERVICE_URL": getenv("USER_SERVICE_URL", ""),
    "LISTING_SERVICE_URL": getenv("LISTING_SERVICE_URL", ""),
}


routing_table = {
    "/users": ENV["USER_SERVICE_URL"],
    "/auth": ENV["USER_SERVICE_URL"],
    "/listing": ENV["LISTING_SERVICE_URL"],
}
