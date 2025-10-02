# Project Requirements – Accounts Mini-Service

## Overview
You are asked to build a small **Accounts Mini-Service** using **Python, FastAPI, and SQLAlchemy**.  
The project should demonstrate **productionization patterns** discussed in the provided theory document.  
The service will be run locally only (no AWS, no cloud services).  
Caching must use **local in-memory cache** (e.g., `functools.lru_cache`).

---

## Functional Requirements

### 1. Account API (CRUD)
- `POST /accounts` – create account (`id`, `name`, `type`, `email`).  
- `GET /accounts/{id}` – fetch account by ID.  
- `GET /accounts?type=...&q=...` – list accounts with optional filters.  
- `PUT /accounts/{id}` – update account.  
- `DELETE /accounts/{id}` – delete account.

### 2. Reference Data API
- `GET /reference/account-types`  
- Returns a small static list, e.g.:  
  ```json
  ["SAVINGS", "CURRENT", "BROKERAGE"]
  ```
- Must be cached in memory with `@lru_cache`.

### 3. Email Notification
- On account creation, call an **email service interface**.
- **dev profile** → mock service prints to console.  
- **prod profile** → service writes email logs to a local file.  
- Selection is **environment-specific** (via config + factory).

### 4. Health API
- `GET /health` → must return service status + database connectivity check.

---

## Non-Functional Requirements

### Environment Profiles
- Use two `.env` files: `.env.dev` and `.env.prod`.
- All config (database URL, log level, env name, etc.) must come from environment variables.

### Typed Configuration + Caching
- Define an `AppSettings` class using **Pydantic Settings**.
- Expose via a `get_settings()` function wrapped in `@lru_cache`.

### Database Layer
- Use **SQLite** (file-based) with **SQLAlchemy**.  
- Create a single engine on startup.  
- Use a request-scoped session (`sessionmaker` + `get_db()` dependency).  
- Ensure proper session closing after each request.

### Caching
- Use `@lru_cache` for:
  1. Settings (`get_settings()`)  
  2. Reference account types endpoint  

### Logging
- Implement structured JSON logging.  
- Each log entry should include: timestamp, log level, request path, status, and duration.

### Dependency Injection
- Use `Depends(get_settings)` and `Depends(get_db)` throughout the app.  
- Provide at least one unit test that overrides a dependency (settings or DB).

### Health & Readiness
- `/health` should check DB connectivity with a lightweight query.

---

## Technical Constraints
- Python 3.11+  
- FastAPI, SQLAlchemy 2.x, Pydantic Settings  
- No external services (AWS, Redis, SMTP, etc.)  
- Only local file system and console output allowed  

---

## Deliverables
1. **Source Code** with a clean structure. Suggested layout:
   ```
   app/
     api/            # Routers: accounts, reference, health
     core/           # config, logging, DI, email service
     db/             # models, session
     main.py
   tests/
   .env.dev
   .env.prod
   requirements.txt / pyproject.toml
   README.md
   requirements.md   # (this file)
   ```
2. **README.md** with setup/run instructions (`uvicorn app.main:app --reload`).
3. **Sample .env.dev and .env.prod** files (no secrets).
4. **At least one test** showing dependency override.
5. **Design Notes**: 1–2 pages mapping implementation choices to productionization patterns.

---

## Evaluation Criteria
- ✅ Correctness of CRUD and endpoints.  
- ✅ Use of productionization patterns:  
  - Environment profiles  
  - Typed config + `@lru_cache`  
  - Engine/session per request  
  - Local caching for reference data  
  - Structured logging  
  - Health endpoint  
- ✅ Code quality (layering, typing, docstrings).  
- ✅ Testability (dependency override).  
- ✅ Clarity of documentation.
