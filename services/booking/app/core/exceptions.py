from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException


class BaseHttpException(StarletteHTTPException):
    def __init__(self, code: int = 500, message="Internal Server Error"):
        self.message = message
        self.status_code = code


class InvalidInputException(BaseHttpException):
    def __init__(self, message="Invalid input"):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message


class NotFoundException(BaseHttpException):
    def __init__(self, message="Ressource not found"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message


class AlreadyExistsException(BaseHttpException):
    def __init__(self, message="Resource already exists"):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = message
