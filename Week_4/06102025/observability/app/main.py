from fastapi import FastAPI, Request, Response, status # type: ignore
from fastapi.responses import JSONResponse, PlainTextResponse # type: ignore
from prometheus_client import Counter, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest # type: ignore
from .models import TransferRequest, LoginRequest
from .logging_utils import configure_json_logging, set_correlation_id, log_event
import random

app = FastAPI(title="Personal Banking Observability")

# Configure logging
configure_json_logging()

# Prometheus registry and counters
registry = CollectorRegistry()
LOGIN_ATTEMPTS = Counter(
    "login_attempts_total",
    "Total number of login attempts",
    ["status"],
    registry=registry
)

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    # Set or create correlation id
    cid = request.headers.get("X-Correlation-Id")
    cid = set_correlation_id(cid)
    # Ensure response propagates it
    response: Response = await call_next(request)
    response.headers["X-Correlation-Id"] = cid
    return response

@app.post("/transfer")
async def transfer(req: TransferRequest):
    ctx = {
        "transactionId": __import__("uuid").uuid4().hex,
        "userId": req.userId,
        "fromAccount": req.fromAccount,
        "toAccount": req.toAccount,
        "amount": req.amount
    }
    log_event(20, "Transaction initiated", **ctx)  # INFO

    if req.amount > 10000:
        ctx["reason"] = "Exceeds transfer limit"
        log_event(40, "Transaction failed", **ctx)  # ERROR
        return JSONResponse({"status": "FAILED", "reason": "Exceeds transfer limit"}, status_code=400)
    else:
        ctx["status"] = "Completed"
        log_event(20, "Transaction successful", **ctx)  # INFO
        return {"status": "COMPLETED"}

@app.post("/login")
async def login(req: LoginRequest):
    if req.username == "admin" and req.password == "password":
        LOGIN_ATTEMPTS.labels(status="success").inc()
        return {"message": f"Login successful for {req.username}"}
    else:
        LOGIN_ATTEMPTS.labels(status="failure").inc()
        return JSONResponse({"message": f"Login failed for {req.username}"}, status_code=401)

@app.get("/health")
async def health():
    ok = random.random() > 0.1
    if ok:
        return {"status": "UP", "components": {"database": {"status": "UP"}}}
    return JSONResponse(
        {"status": "DOWN", "components": {"database": {"status": "DOWN", "error": "Failed to connect to DB"}}},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    )

@app.get("/metrics")
async def metrics():
    data = generate_latest(registry)
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)
