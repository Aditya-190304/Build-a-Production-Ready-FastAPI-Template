import json
import logging

from app.core.logging.formatters import JsonFormatter


def test_json_formatter_outputs_structured_payload() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="app.request",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Request completed",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-123"
    record.method = "GET"
    record.path = "/api/v1/health"
    record.status_code = 200
    record.duration_ms = 12.5

    payload = json.loads(formatter.format(record))

    assert payload["logger"] == "app.request"
    assert payload["message"] == "Request completed"
    assert payload["request_id"] == "req-123"
    assert payload["method"] == "GET"
    assert payload["path"] == "/api/v1/health"
    assert payload["status_code"] == 200
