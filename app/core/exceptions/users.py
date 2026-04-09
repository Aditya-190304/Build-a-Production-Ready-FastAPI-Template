from fastapi import status

from app.core.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    message = "A user with this email already exists."
