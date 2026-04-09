from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.core.exceptions.base import ErrorDetail

HTTP_ERROR_CODES = {
    status.HTTP_400_BAD_REQUEST: "bad_request",
    status.HTTP_401_UNAUTHORIZED: "unauthorized",
    status.HTTP_403_FORBIDDEN: "forbidden",
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_409_CONFLICT: "conflict",
    status.HTTP_422_UNPROCESSABLE_CONTENT: "validation_error",
}


def register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details = [
            ErrorDetail(
                field=".".join(str(part) for part in error["loc"]),
                message=error["msg"],
                type=error["type"],
            )
            for error in exc.errors()
        ]
        return _error_response(
            request=request,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            code="validation_error",
            message="Request validation failed.",
            details=details,
        )

    @application.exception_handler(AppException)
    async def handle_application_exception(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        return _error_response(
            request=request,
            status_code=exc.status_code,
            code=exc.code,
            message=exc.message,
            details=exc.details,
            headers=exc.headers,
        )

    @application.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        return _error_response(
            request=request,
            status_code=exc.status_code,
            code=HTTP_ERROR_CODES.get(exc.status_code, "http_error"),
            message=str(exc.detail),
            details=[],
            headers=exc.headers,
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request,
        _: Exception,
    ) -> JSONResponse:
        return _error_response(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="internal_server_error",
            message="An unexpected error occurred.",
            details=[],
        )


def _error_response(
    *,
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: list[ErrorDetail],
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    payload = {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id,
            "details": [detail.to_dict() for detail in details],
        }
    }
    response_headers = dict(headers or {})
    response_headers.setdefault("X-Request-ID", request_id)
    return JSONResponse(status_code=status_code, content=payload, headers=response_headers)
