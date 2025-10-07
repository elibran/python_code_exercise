import json
import logging
import os
import time
from typing import Any, Dict, Optional
from contextvars import ContextVar

# Correlation/request id stored per-request
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

def set_correlation_id(value: Optional[str]) -> None:
    correlation_id_ctx.set(value)

def get_correlation_id() -> Optional[str]:
    return correlation_id_ctx.get()

class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter without extra dependencies."""
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)) + f".{int(record.msecs):03d}Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include correlation_id if present
        cid = get_correlation_id()
        if cid:
            payload["correlation_id"] = cid

        # Attach standard extras if present
        for key in ("path", "method", "status_code", "duration_ms", "user_id", "order_id"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        # Include exception info if any
        if record.exc_info:
            payload["exc_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
            payload["exc_message"] = str(record.exc_info[1]) if record.exc_info[1] else None

        return json.dumps(payload, ensure_ascii=False)

def configure_logging(level: Optional[str] = None) -> None:
    """Configure root and uvicorn loggers to emit JSON."""
    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()

    # Clear handlers to avoid duplicates on reload
    for logger_name in ("", "uvicorn", "uvicorn.error", "uvicorn.access", "sqlalchemy.engine"):
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(lvl)
    root.addHandler(handler)

    # Uvicorn loggers
    logging.getLogger("uvicorn").setLevel(lvl)
    logging.getLogger("uvicorn.error").addHandler(handler)
    logging.getLogger("uvicorn.error").setLevel(lvl)
    logging.getLogger("uvicorn.access").addHandler(handler)
    logging.getLogger("uvicorn.access").setLevel(lvl)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
