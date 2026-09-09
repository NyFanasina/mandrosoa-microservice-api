from uuid import UUID

from fastapi import APIRouter, Request

from ..core.dependencies import UserServiceDeps
from ..model import UserAdminUpdate, UserCreate, UserResponse, UserUpdate
from ..schemas import ApiResponse
from ..security import AdminGuardDeps, UserGuardDeps

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("", response_model=ApiResponse[list[UserResponse]])
def get_user_list(service: UserServiceDeps, _: AdminGuardDeps):
    return service.index()


@user_router.post("", response_model=ApiResponse[UserResponse])
def create_user(user: UserCreate, auth_service: UserServiceDeps, request: Request, _: AdminGuardDeps):
    return auth_service.register(user, str(request.base_url))


@user_router.put("/me", response_model=ApiResponse[UserResponse])
def update_me(user_data: UserUpdate, service: UserServiceDeps, current_user: UserGuardDeps):
    return service.update(current_user["id_user"], user_data)


@user_router.get("/{user_id}", response_model=ApiResponse[UserResponse])
def find_user_by_id(user_id: UUID, service: UserServiceDeps, _: AdminGuardDeps):
    return service.show(user_id)


@user_router.put("/{user_id}", response_model=ApiResponse[UserResponse])
def update_user(user_id: UUID, user_data: UserAdminUpdate, service: UserServiceDeps, _: AdminGuardDeps):
    return service.update(user_id, user_data)


@user_router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserServiceDeps, _: AdminGuardDeps):
    return service.destroy(user_id)
