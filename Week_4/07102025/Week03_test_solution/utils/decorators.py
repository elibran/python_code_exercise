import time
from functools import wraps
from utils.logging import get_logger

logger = get_logger(__name__)

def log_operation(operation_name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return fn(*args, **kwargs)
            finally:
                duration_ms = int((time.time() - start) * 1000)
                logger.info("operation_timing", extra={"duration_ms": duration_ms})
        return wrapper
    return decorator
