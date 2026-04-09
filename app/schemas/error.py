from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    field: str | None = Field(default=None, examples=["body.email"])
    message: str = Field(..., examples=["value is not a valid email address"])
    type: str | None = Field(default=None, examples=["value_error"])


class ErrorEnvelope(BaseModel):
    code: str = Field(..., examples=["validation_error"])
    message: str = Field(..., examples=["Request validation failed."])
    request_id: str = Field(..., examples=["2ee56d4b-859b-426d-9f0b-23ec6cc8db4b"])
    details: list[ErrorDetail] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    error: ErrorEnvelope

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": {
                    "code": "validation_error",
                    "message": "Request validation failed.",
                    "request_id": "2ee56d4b-859b-426d-9f0b-23ec6cc8db4b",
                    "details": [
                        {
                            "field": "body.email",
                            "message": "value is not a valid email address",
                            "type": "value_error",
                        }
                    ],
                }
            }
        }
    )
