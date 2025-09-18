# Light Banking API (FastAPI)

A minimal, easy-to-read version of the Personal Banking API with just **three** endpoints:

- `GET /v1/health` — health check
- `POST /v1/customers/` — create a customer
- `POST /v1/accounts/` — create a bank account for a customer

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Open http://127.0.0.1:8000/v1/docs
```

## Example requests

### 1) Create a Customer
```bash
curl -X POST "http://127.0.0.1:8000/v1/customers/"   -H "Content-Type: application/json"   -d '{"name":"Rahul"}'
```

### 2) Create an Account
```bash
curl -X POST "http://127.0.0.1:8000/v1/accounts/"   -H "Content-Type: application/json"   -d '{
    "account_type": "SAVINGS",
    "balance": 500.0,
    "customer_id": 1
  }'
```

### 3) Health
```bash
curl "http://127.0.0.1:8000/v1/health"
```

## Project Layout

```
light_banking_api/
├─ banking.db            # SQLite (created on first run)
├─ requirements.txt
├─ README.md
└─ app/
   ├─ __init__.py
   ├─ main.py
   ├─ database.py
   ├─ models.py
   ├─ schemas.py
   └─ services.py
```

## Notes
- SQLite database lives at the project root for simplicity.
- For production, replace `create_all` with migrations (Alembic) and move to Postgres/MySQL.
