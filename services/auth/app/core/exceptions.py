from fastapi import HTTPException, status


class BaseHttpException(HTTPException):
    def __init__(self, code: int = 500, message="Internal Server Error"):
        self.message = message
        self.status_code = code


class NotFoundException(BaseHttpException):
    def __init__(self, message="Ressource not found"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message


class AlreadyExistsException(BaseHttpException):
    def __init__(self, message="Resource already exists"):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = message


class UnAuthorizedException(BaseHttpException):
    def __init__(self, message="Unauthorized"):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
