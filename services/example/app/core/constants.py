from os import getenv

from dotenv import load_dotenv

load_dotenv()

ENV = {
    "SECRET_KEY": getenv("SECRET_KEY"),
}
