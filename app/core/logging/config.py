import logging
import logging.config

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    formatter_class = (
        "app.core.logging.formatters.JsonFormatter"
        if settings.log_json
        else "logging.Formatter"
    )
    formatter_config: dict[str, object] = {
        "()": formatter_class,
    }
    if not settings.log_json:
        formatter_config["format"] = "%(asctime)s %(levelname)s %(name)s %(message)s"

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": formatter_config,
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "level": settings.effective_log_level,
                "handlers": ["default"],
            },
        }
    )
