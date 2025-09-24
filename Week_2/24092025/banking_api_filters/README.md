# Banking API (v1.2)

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



## API Versioning (Added in v1.1)

This release introduces **path-based versioning** with minimal changes to the existing code. 
All existing routes continue to work unversioned (backward compatibility), and the same functionality
is now also available under the new **`/api/v1`** prefix.

### Examples

- Health/Root:
  - `GET /` (existing)
- Accounts:
  - `POST /accounts/` (existing)
  - `POST /api/v1/accounts/` (new, versioned equivalent)
  - `GET /api/v1/accounts/{account_id}`
  - `POST /api/v1/accounts/{from_id}/transfer/{to_id}`
  - `GET /api/v1/accounts/{account_id}/kyc`
  - `PUT /api/v1/accounts/{account_id}/kyc`

### Why this approach?
- **Minimal change**: No edits to existing routers, schemas, services, or repositories.
- **Add-only**: We added `app/api/v1/__init__.py` and a couple of lines in `app/main.py` to include the versioned router.
- **Backward compatible**: Your current clients can keep using existing paths while newer clients switch to `/api/v1/...`.

### How to run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then visit:
- http://127.0.0.1:8000/docs for interactive Swagger UI (you will see both versioned and unversioned paths).


## Transactions API – Filtering, Sorting, Pagination (v1.2)

**Endpoint**  
`GET /accounts/{accountId}/transactions`

**Query Parameters**
- `status` *(optional)*: Filter by status (e.g., `completed`, `pending`, `failed`)
- `sortBy` *(optional)*: Format `field:direction`; fields: `date`, `amount`, `id`, `status`; direction: `asc` or `desc`  
  Example: `sortBy=date:desc`
- `page` *(optional, default=1)*: Page number (1-based)
- `limit` *(optional, default=25, max=100)*: Page size

**Examples**

- First 50 completed transactions, newest first
```bash
curl -G "http://localhost:8000/accounts/1/transactions"   --data-urlencode "status=completed"   --data-urlencode "sortBy=date:desc"   --data-urlencode "page=1"   --data-urlencode "limit=50"
```

- Pending transactions, sort by amount ascending, page 2 with 10 per page
```bash
curl -G "http://localhost:8000/accounts/1/transactions"   --data-urlencode "status=pending"   --data-urlencode "sortBy=amount:asc"   --data-urlencode "page=2"   --data-urlencode "limit=10"
```

**Notes**
- If `limit` is not provided, a default of **25** is used.
- A maximum `limit` of **100** is enforced to protect server performance.
- Sorting defaults to `date ASC` when `sortBy` is omitted or invalid.

### Testing
Run pytest (uses your dev DB connection):
```bash
pytest tests/test_transactions.py -q
```
