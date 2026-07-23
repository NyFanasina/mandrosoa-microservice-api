from fastapi import APIRouter

router = APIRouter(prefix="")


@router.get("/")
def read_root():
    return {"Hello": "World"}
