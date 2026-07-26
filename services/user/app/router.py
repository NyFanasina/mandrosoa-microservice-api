from typing import Annotated

from fastapi import APIRouter, Depends

from .core.dependencies import get_user_service
from .model import UserCreate, UserUpdate
from .service import UserService

router = APIRouter(prefix="/users", tags=["User"])

user_service_deps = Annotated[UserService, Depends(get_user_service)]


@router.get("/")
def get_user_list(service: user_service_deps):
    return service.index()


@router.post("/")
def register_user(user: UserCreate, service: user_service_deps):
    return service.create(user)


@router.get("/{user_id}")
def find_user_by_id(user_id: str, service: user_service_deps):
    return service.show(user_id)


@router.put("/{user_id}")
def update_user(user_id: str, user_data: UserUpdate, service: user_service_deps):
    return service.update(user_id, user_data)


@router.delete("/{user_id}")
def delete_user(user_id: str, service: user_service_deps):
    return service.destroy(user_id)
