from os import getenv

from dotenv import load_dotenv

loaded = load_dotenv()

if not loaded:
    raise Exception("Please create a .env file")

ENV = {
    "JWT_SECRET_KEY": getenv("JWT_SECRET_KEY"),
    "JWT_ALGORITHM": getenv("JWT_ALGORITHM", "HS256"),
    "COOKIE_NAME": str(getenv("COOKIE_NAME")),
    "HTTPONLY": getenv("HTTPONLY", "false").lower() == "true",
    "SECURE": getenv("SECURE", "false").lower() == "true",
    "SAMESITE": getenv("SAMESITE"),
    "TOKEN_EXPIRE_IN": int(getenv("TOKEN_EXPIRE_IN") or 30),
    "DATABASE_URL": getenv("DATABASE_URL"),
    "BREVO_API_KEY": getenv("BREVO_API_KEY"),
    "BREVO_SENDER_NAME": getenv("BREVO_SENDER_NAME"),
    "BREVO_SENDER_EMAIL": getenv("BREVO_SENDER_EMAIL"),
}
