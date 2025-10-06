# Observability in Personal Banking (FastAPI)

FastAPI app that demonstrates **structured logging**, **metrics**, and **health checks**.

## Features
- JSON logs with correlation IDs (`X-Correlation-Id` header)
- `/transfer` POST endpoint implementing structured transaction logging
- `/login` POST endpoint with Prometheus counters for success/failure
- `/health` readiness-style endpoint
- `/metrics` Prometheus scrape endpoint

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Try it
```bash
# Transfer (success / failure)
curl -X POST http://localhost:8080/transfer -H 'Content-Type: application/json'   -d '{"userId":"user-abc-123","fromAccount":"ACCT-001","toAccount":"ACCT-002","amount":500}'

curl -X POST http://localhost:8080/transfer -H 'Content-Type: application/json'   -d '{"userId":"user-def-456","fromAccount":"ACCT-003","toAccount":"ACCT-004","amount":15000}'

# Login
curl -X POST http://localhost:8080/login -H 'Content-Type: application/json'   -d '{"username":"admin","password":"password"}'

curl -X POST http://localhost:8080/login -H 'Content-Type: application/json'   -d '{"username":"hacker","password":"guess"}'

# Health
curl http://localhost:8080/health

# Metrics
curl http://localhost:8080/metrics
```


---

## How to Run (Local)

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

**Key Endpoints**
- `POST /login` — increments `login_attempts_total` with status label.
- `POST /transfer` — validates amount, logs structured events.
- `GET /health` — returns 200/UP or 503/DOWN.
- `GET /metrics` — Prometheus text exposition format.

**Quick Smoke Test**
```bash
# Health
curl -i http://localhost:8080/health

# Metrics
curl -i http://localhost:8080/metrics

# Login (success)
curl -i -X POST http://localhost:8080/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"password"}'

# Login (failure)
curl -i -X POST http://localhost:8080/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"wrong"}'

# Transfer (success)
curl -i -X POST http://localhost:8080/transfer -H 'Content-Type: application/json' -d '{"userId":"u1","fromAccount":"A","toAccount":"B","amount":42}'

# Transfer (limit breach)
curl -i -X POST http://localhost:8080/transfer -H 'Content-Type: application/json' -d '{"userId":"u1","fromAccount":"A","toAccount":"B","amount":10001}'
```

**Correlation ID**
```bash
curl -i -H 'X-Correlation-Id: demo-123' http://localhost:8080/health
# Response will include 'X-Correlation-Id: demo-123'
```

## Run Tests

```bash
pip install pytest httpx
pytest -q
```
