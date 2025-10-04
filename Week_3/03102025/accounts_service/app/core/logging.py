import json
import logging
import time
from typing import Callable
from fastapi import Request, Response

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
    )

async def request_logger_middleware(request: Request, call_next: Callable):
    start = time.time()
    response: Response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    record = {
        "event": "http_request",
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    }
    logging.getLogger("uvicorn.access").info(json.dumps(record))
    return response
