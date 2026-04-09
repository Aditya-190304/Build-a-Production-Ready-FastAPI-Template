from dataclasses import asdict, dataclass

from fastapi import status


@dataclass(slots=True)
class ErrorDetail:
    message: str
    field: str | None = None
    type: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


class AppException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "application_error"
    message = "Request failed."

    def __init__(
        self,
        message: str | None = None,
        *,
        details: list[ErrorDetail] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details or []
        self.headers = headers or {}
        super().__init__(self.message)
