from os import getenv

from dotenv import load_dotenv

load_dotenv()

ENV = {
    "SECRET_KEY": getenv("SECRET_KEY"),
    "COOKIE_NAME": str(getenv("COOKIE_NAME")),
    "TOKEN_EXPIRE_IN": int(getenv("TOKEN_EXPIRE_IN") or 30),
}
