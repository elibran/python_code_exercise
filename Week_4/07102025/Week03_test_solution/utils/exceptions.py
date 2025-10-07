from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.logging import get_logger

logger = get_logger(__name__)

class AppException(Exception):
    def __init__(self, message: str):
        self.message = message

class PaymentFailed(AppException):
    pass

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning("app_exception", extra={"path": request.url.path})
        return JSONResponse(status_code=400, content={"error": exc.message})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Standardize shape while preserving code
        logger.warning("http_exception", extra={"path": request.url.path, "status_code": exc.status_code})
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("validation_error", extra={"path": request.url.path})
        return JSONResponse(status_code=422, content={"error": "Validation error", "details": exc.errors()})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception", extra={"path": request.url.path})
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
