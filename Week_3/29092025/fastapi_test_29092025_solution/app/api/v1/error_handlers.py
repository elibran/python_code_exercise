from fastapi import FastAPI, Request # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR # type: ignore

def _json_safe_errors(errs):
    safe = []
    for e in errs:
        e = e.copy()
        ctx = e.get("ctx")
        if isinstance(ctx, dict):
            e["ctx"] = {k: (v if isinstance(v, (str, int, float, bool)) or v is None else str(v)) for k, v in ctx.items()}
        safe.append(e)
    return safe

def init_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": _json_safe_errors(exc.errors())})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
