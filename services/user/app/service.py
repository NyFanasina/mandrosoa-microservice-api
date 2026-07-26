from sqlalchemy.exc import IntegrityError

from .core.exceptions import AlreadyExistsException, NotFoundException
from .model import User, UserCreate, UserUpdate
from .repository import UserRepository
from .utils import format_response


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def index(self):
        return format_response(data=self.repository.all(), message="List of users")

    def create(self, user: UserCreate):
        try:
            next_user = User.model_validate(user)
            data = self.repository.create(next_user)
            return format_response(201, data, "User registered")

        except IntegrityError as e:
            raise AlreadyExistsException(message=str(e.orig))

    def show(self, user_id: str):
        user = self.repository.findById(user_id)

        if user is None:
            raise NotFoundException(message="User Not Found")

        return format_response(data=user, message="User found")

    def update(self, user_id: str, user: UserUpdate):
        db_user = self.repository.findById(user_id)

        if db_user is None:
            raise NotFoundException("User Not Found")

        new_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(new_data)
        data = self.repository.update(db_user)
        return format_response(200, data, "User Updated")

    def destroy(self, user_id: str):
        user = self.repository.findById(user_id)

        if user is None:
            raise NotFoundException("User Not Found")

        self.repository.remove(user)
        return format_response(message="User Deleted")
