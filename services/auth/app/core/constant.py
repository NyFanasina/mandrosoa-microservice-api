from os import getenv

from dotenv import load_dotenv

loaded = load_dotenv()

if not loaded:
    raise Exception("Please create a .env file")

ENV = {
    "SECRET_KEY": getenv("SECRET_KEY"),
    "COOKIE_NAME": str(getenv("COOKIE_NAME")),
    "HTTPONLY": getenv("HTTPONLY", "false").lower() == "true",
    "SECURE": getenv("SECURE", "false").lower() == "true",
    "SAMESITE": getenv("SAMESITE"),
    "TOKEN_EXPIRE_IN": int(getenv("TOKEN_EXPIRE_IN") or 30),
    "DATABASE_URL": getenv("DATABASE_URL"),
}
