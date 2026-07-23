from fastapi import FastAPI
from app.router import router
from dotenv import load_dotenv
from app.database import init_database

load_dotenv()
init_database()

app = FastAPI()
app.include_router(router)
