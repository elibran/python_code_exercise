# FIL Order Service – Refined Solution (Structured Logging + Robust Error Handling)

This update adds **structured JSON logging**, **correlation IDs**, and **comprehensive error handling** while preserving all existing behavior and tests.

## Highlights
- **JSON logs** (no extra deps): consistent key/value logs.
- **Correlation ID** (`X-Request-ID`): auto-generated if missing and echoed back in the response.
- Request logging middleware with **duration (ms)**, method, path, status.
- Endpoint-level **audit logs** (login, register, create order, list, get).
- Centralized exception handlers for `AppException`, `HTTPException`, `RequestValidationError`, and a safe 500 fallback.
- **Pydantic v2**-friendly (`ConfigDict(from_attributes=True)`).
- **FastAPI lifespan** used instead of deprecated `on_event`.

## Quick Start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open: http://127.0.0.1:8000/docs

## ENV
- `LOG_LEVEL` → default `INFO`
- `SECRET_KEY` → default `dev-secret-key-change-me`
- `DATABASE_URL` → default `sqlite:///./app.db`

## Tests
```bash
pytest -v -s
```

## Example log line
```json
{"time":"2025-10-05T12:00:00.123Z","level":"INFO","logger":"utils.logging","message":"request_completed","correlation_id":"6f34...","path":"/orders","method":"POST","status_code":201,"duration_ms":62}
```
