# Accounts Mini-Service (FastAPI)

A local-only FastAPI service demonstrating productionization concepts: environment profiles, 
typed config, cached settings, DI, SQLAlchemy sessions, local LRU caching, 
structured logging, env-specific services, and health checks.

---

## 1) Features Overview
- Accounts CRUD with SQLite + SQLAlchemy 2.x
- Reference data endpoint cached via `functools.lru_cache`
- Auto-selects **.env** file by `APP_ENV` environment variable:
  - `APP_ENV=development` → loads `.env.dev` (default)
  - `APP_ENV=production`  → loads `.env.prod`
- Structured JSON HTTP logs
- Additional per-endpoint logs (create/update/delete, health, reference)
- Email service abstraction (dev → console, prod → file)
- Unit tests using in-memory SQLite

---

## 2) Prerequisites
- Python 3.11+
- (Optional) Virtual environment

---

## 3) Setup
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# or CMD
# .venv\Scripts\activate
# or Unix/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

---

## 4) Environment selection (auto .env loading)

The app loads a dotenv file based on the OS environment variable `APP_ENV` **before** settings are created.

### Cases
- **No `APP_ENV` set** → defaults to `development` → loads `.env.dev`
- **`APP_ENV=development` or `dev`** → loads `.env.dev`
- **`APP_ENV=production` or `prod`** → loads `.env.prod`

### Examples
**Windows PowerShell**
```powershell
# Case 1: default dev
Remove-Item Env:APP_ENV -ErrorAction SilentlyContinue
uvicorn app.main:app --reload

# Case 2: explicitly dev
$env:APP_ENV = "development"
uvicorn app.main:app --reload

# Case 3: prod-like local
$env:APP_ENV = "production"
uvicorn app.main:app --reload
```

**bash/zsh**
```bash
# default dev
unset APP_ENV
uvicorn app.main:app --reload

# dev
set APP_ENV=development 
uvicorn app.main:app --reload

# prod-like
set APP_ENV=production 
uvicorn app.main:app --reload
```

---

## 5) Run the app
```bash
uvicorn app.main:app --reload
# or choose port
uvicorn app.main:app --port 5001 --reload
```
Open docs: http://127.0.0.1:8000/docs

> The app will create SQLite files under `./data/` if using file-based DB URLs from the env files.

---

## 6) Endpoints
- `POST /accounts` – create account
- `GET /accounts/{id}` – get by id
- `GET /accounts?type=...&q=...` – list with filters
- `PUT /accounts/{id}` – update
- `DELETE /accounts/{id}` – delete
- `GET /reference/account-types` – cached reference values
- `GET /health` – service + DB check

---

## 7) Tests
```bash
pytest -q
```
- Uses **in-memory SQLite** with shared `StaticPool`
- Overrides `get_db()` dependency
- Tests cover health, reference, and CRUD flow

---

## 8) Logs
- HTTP JSON logs (method, path, status_code, duration_ms)
- Endpoint logs using module loggers
- Configurable level via `LOG_LEVEL` (`DEBUG` for dev, `INFO` for prod)

---

## 9) Constraints
- Local execution only
- No AWS/Redis/SMTP; only file system + console
