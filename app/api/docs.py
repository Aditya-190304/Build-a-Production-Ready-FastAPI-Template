from app.schemas.error import ErrorResponse


def error_response_doc(
    *,
    description: str,
    code: str,
    message: str,
    status_code: int,
    details: list[dict[str, str | None]] | None = None,
) -> dict[int, dict[str, object]]:
    return {
        status_code: {
            "model": ErrorResponse,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": code,
                            "message": message,
                            "request_id": "2ee56d4b-859b-426d-9f0b-23ec6cc8db4b",
                            "details": details or [],
                        }
                    }
                }
            },
        }
    }
