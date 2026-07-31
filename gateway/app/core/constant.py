from os import getenv

from dotenv import load_dotenv

loaded = load_dotenv()

if not loaded:
    raise Exception("Please create a .env file")

ENV = {
    "USER_SERVICE_URL": str(getenv("USER_SERVICE_URL")),
}


routing_table = {
    "/users": ENV["USER_SERVICE_URL"],
    "/auth": ENV["USER_SERVICE_URL"],
}
