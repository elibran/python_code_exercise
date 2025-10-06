import json
import logging
import time
import uuid
from contextvars import ContextVar

CORRELATION_ID: ContextVar[str] = ContextVar("correlation_id", default="")

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # Collect known attributes and any extras
        payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlationId": getattr(record, "correlationId", CORRELATION_ID.get(""))
        }
        # Include all custom attributes under 'context'
        context = getattr(record, "context", {})
        if context:
            payload["context"] = context
        return json.dumps(payload, ensure_ascii=False)

class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Inject correlation id into the record
        cid = CORRELATION_ID.get("")
        if not getattr(record, "correlationId", None):
            record.correlationId = cid
        return True

def configure_json_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(level)
    # Avoid duplicate handlers if reloaded
    root.handlers = []
    root.addHandler(handler)
    root.addFilter(CorrelationIdFilter())

def set_correlation_id(value: str | None) -> str:
    if not value:
        value = str(uuid.uuid4())
    CORRELATION_ID.set(value)
    return value

def log_event(level: int, message: str, **context):
    logging.getLogger("app").log(level, message, extra={"context": context})
