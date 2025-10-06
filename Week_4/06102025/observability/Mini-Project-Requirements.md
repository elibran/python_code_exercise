# Mini Project Requirements — Observability-ready Personal Banking API

This mini-project turns the provided FastAPI app into a hands-on lab for **Observability & Support** concepts:

- **Structured JSON logging** with correlation IDs

```json
{
  "timestamp": "2025-10-04T14:24:15",
  "level": "INFO",
  "logger": "app",
  "message": "Transaction successful",
  "correlationId": "87183c36-15d0-4197-82f2-82594006c3ed",
  "context": {
    "transactionId": "a4e813eeea044476bc15e0f8e5d5216c",
    "userId": "u1",
    "fromAccount": "A",
    "toAccount": "B",
    "amount": 5000.0,
    "status": "Completed"
  }
}
```

- **Metrics instrumentation** with Prometheus

```text
# HELP login_attempts_total Total number of login attempts
# TYPE login_attempts_total counter
login_attempts_total{status="success"} 4.0
login_attempts_total{status="failure"} 1.0
```

- **Gauge data (auto-generated creation timestamps)**

```text
# HELP login_attempts_created Total number of login attempts
# TYPE login_attempts_created gauge
login_attempts_created{status="success"} 1.759586051317564e+09
login_attempts_created{status="failure"} 1.7595860626108625e+09
```

- **Health checks** with proper status codes

```json
{
  "status": "UP",
  "components": {
    "database": {
      "status": "UP"
    }
  }
}
```

- **Verification via pytest**

---

These map to the three pillars described in the slide deck “012_Observability & Support-Concepts.pdf”:

1. **Centralised Logging** — use structured, contextual logs and a `correlationId` to follow requests end-to-end.  
2. **Metrics Instrumentation** — expose counters and scrapeable metrics for operational insights.  
3. **Health Checks & Alerting** — provide a `/health` endpoint that signals readiness (200) vs unavailability (503).

---

## Functional Scope

### 1️⃣ Authentication — `/login` (POST)
- Accepts `username`, `password`.
- Increments Prometheus **Counter** `login_attempts_total{status="success|failure"}`.
- Returns 200 on success, 401 on failure.

### 2️⃣ Money Transfer — `/transfer` (POST)
- Accepts `userId`, `fromAccount`, `toAccount`, `amount`.
- Emits structured JSON logs for **initiated**, **failed**, and **successful** transfers.
- Rejects amounts `> 10000` with HTTP 400 and reason “Exceeds transfer limit”.

### 3️⃣ Health — `/health` (GET)
- Returns `{"status": "UP"}` with HTTP 200 when healthy.  
- Returns `{"status": "DOWN"}` with HTTP **503** when unhealthy (simulated DB failure).

### 4️⃣ Metrics — `/metrics` (GET)
- Exposes Prometheus metrics via `prometheus_client.generate_latest`  
  with content type `text/plain; version=0.0.4; charset=utf-8`.

### 5️⃣ Correlation ID (Middleware)
- Reads `X-Correlation-Id` header, generates one if absent,  
  and **echoes it back** in the response header.  
- The same ID is injected into all structured logs.

---

## Non-Functional & Observability Requirements

- **Structured JSON logs** using a custom `JsonFormatter` (see `app/logging_utils.py`).  
  Each log record MUST include:
  - `timestamp`, `level`, `logger`, `message`
  - `correlationId`
  - `context` (e.g., userId, transactionId, amount, status, reason)

- **Log levels**  
  - Use `INFO` for normal flow, `ERROR` for failures.

- **Metrics coverage**  
  - `login_attempts_total{status=success|failure}` counter increments per login attempt outcome.

- **Health semantics**  
  - HTTP **503** must be used when unhealthy to signal load balancers and orchestrators correctly.

- **Portability**  
  - App must run with:  
    ```bash
    uvicorn app.main:app --reload --port 8080
    ```

---

## Deliverables

1. **Updated `README.md`** with run instructions, endpoints, and local verification steps.  
2. **`Mini-Project-Requirements.md`** (this file).  
3. **`verification.md`** — step-by-step pytest execution and what each test validates.  
4. **Pytest suite** under `tests/` to verify logging, metrics, health, correlation ID, and business rules.  
5. **Project zip** with tests and documentation for distribution.

---

## Slide-based Concept Primer (for hands-on context)

### 📘 Structured Logging  
*(Slides: “Centralised Logging”, “Logging Best Practices”)*  
- Use JSON logs for searchability and correlation across microservices.  
- Always include a `correlationId` and relevant domain IDs (`userId`, `transactionId`, etc.).

### 📊 Metrics  
*(Slides: “Metrics Instrumentation”, “Key Tools”, “/metrics output”)*  
- Use counters for login attempts; expose `/metrics` for Prometheus.

### ❤️ Health & Alerting  
*(Slides: “Health Checks & Alerting”)*  
- `GET /health`: return **200/UP** or **503/DOWN**.  
- Use **503** to signal unavailability so load balancers stop routing traffic.

---
