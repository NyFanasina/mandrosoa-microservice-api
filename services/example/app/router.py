from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["HELLO"])


@router.get("/")
def hello():
    return {"message": "Hello World"}
