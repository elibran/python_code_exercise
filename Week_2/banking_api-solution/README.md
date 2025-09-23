# FastAPI Fundamentals — Personal Banking API

Clean layered architecture with **Routers → Services → Repositories**, **SQLAlchemy ORM**, and **Pydantic Settings**.

## Features
- Create account
- Get account by ID
- List all accounts
- Deposit money
- Withdraw money (insufficient funds check)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for Swagger UI.


## New APIs

- Transfer money between two accounts (atomic update)
- Check if an account is KYC compliant

### Examples
```bash
# Transfer 50.0 from account 1 to account 2
curl -X POST http://127.0.0.1:8000/accounts/transfer \
  -H 'Content-Type: application/json' \
  -d '{"from_account_id":1, "to_account_id":2, "amount":50.0}'

# Get KYC status for account 1
curl http://127.0.0.1:8000/accounts/1/kyc-status
```

> Note: A new boolean column `kyc_compliant` was added to the `accounts` table. If you are using the provided SQLite `bank.db` created before this change, delete it to auto-recreate with the new schema, or run a manual migration.


## KYC APIs

### Get KYC Status
**GET** `/accounts/{account_id}/kyc-status`

**200 Response**
```json
{ "account_id": 42, "kyc_compliant": false }
```

**404 Response**
```json
{ "detail": "Account not found" }
```

### Set KYC Status
**PUT** `/accounts/{account_id}/kyc-status`

Idempotently sets the account's KYC status. If no body or query param is provided, it defaults to `true` (mark compliant).

**Request (JSON body)**:
```json
{ "kyc_compliant": true }
```

**Or as query param**: `?kyc_compliant=false`

**200 Response**
```json
{ "account_id": 42, "kyc_compliant": true }
```

**404 Response**
```json
{ "detail": "Account not found" }
```
