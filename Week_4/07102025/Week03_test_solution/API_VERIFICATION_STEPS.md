
# API Verification Guide — FIL Order Service (FastAPI)

**Purpose:** Step‑by‑step verification of every API in a logical order, including success paths, RBAC checks, validation errors, async behavior, and rollback on external failure.

**Applies to repo:** `order_service`  
**Base URL (default):** `http://127.0.0.1:8000`  
**Auth:** Bearer JWT (from `/auth/login`)  
**DB:** SQLite file `./app.db`

---

## 0) Prerequisites & Setup

1. **Create venv & install deps**
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Start the app**
   ```bash
   uvicorn main:app --reload
   ```
   Swagger UI: `http://127.0.0.1:8000/docs`

3. **(Optional) Clean state**
   - Stop the server.
   - Delete `./app.db` and `./notifications.log` if present.
   - Restart `uvicorn`.

> **Note:** On Windows, if deletion fails because files are in use, stop the server first, then retry.

---

## 1) Health Check

**Request**
```bash
curl "http://127.0.0.1:8000/"
```

**Expected Response**
```json
{"status":"ok"}
```

---

## 2) Authentication & Authorization

### 2.1 Register two users (admin & user)

**Admin registration**
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"adminpass\",\"role\":\"admin\"}"
```

**User registration**
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"alice@example.com\",\"password\":\"password123\",\"role\":\"user\"}"
```

**Checks**
- Status code = `201`
- Response has `id`, `email`, `role` fields.
- Duplicate email should return `400` with `{"detail":"Email already registered"}`

### 2.2 Login and capture JWTs

**Admin login**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"adminpass\"}"
```
Copy the `access_token` value.

**User login**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"alice@example.com\",\"password\":\"password123\"}"
```

**Windows PowerShell (set variables)**
```powershell
$ADMIN_TOKEN = "<paste-admin-token>"
$USER_TOKEN  = "<paste-user-token>"
```

**Checks**
- Status code = `200`
- JSON contains `access_token` & `token_type: "bearer"`
- Wrong password → `401 Invalid credentials`

### 2.3 Protected route without token (negative)

```bash
curl "http://127.0.0.1:8000/orders"
```
**Expected**
- Status code = `403` (Not authenticated) from `HTTPBearer`

---

## 3) Orders — Success Transaction Flow

### 3.1 Create order (success) as normal user

```bash
curl -X POST "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"product_id\":\"P123\",\"quantity\":2,\"price\":150.0}"
```
> PowerShell: use `$USER_TOKEN`. CMD: set `%USER_TOKEN%`. On macOS/Linux replace with `$USER_TOKEN`.

**Expected**
- Status code = `201`
- JSON has `status: "confirmed"`, a numeric `id`, and correct payload echo.

### 3.2 Verify async notification

- Wait ~200ms, then check `notifications.log` in the project root.
- Expected new line: `Notified alice@example.com for order <ID>`

(If not present, ensure app is still running and try again; background tasks run after sending the response.)

---

## 4) Orders — Listing & RBAC

### 4.1 List orders as user (should only see self)

```bash
curl "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%"
```
**Expected**
- Status code = `200`
- Array length ≥ 1 (includes the order created in §3)
- **All** items have `user_id` matching the current user.

### 4.2 List orders as admin (should see all)

```bash
curl "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %ADMIN_TOKEN%"
```
**Expected**
- Status code = `200`
- Array length ≥ user’s count
- Items may include orders from multiple users.

---

## 5) Order Retrieval by ID and Access Control

1. From the **user list** response (§4.1), pick an `id` of the order you created.  
   ```powershell
   $ORDER_ID = <paste-id-here>
   ```

2. **Get as owner (user)** — should succeed:
   ```bash
   curl "http://127.0.0.1:8000/orders/%ORDER_ID%" ^
     -H "Authorization: Bearer %USER_TOKEN%"
   ```
   **Expected**: `200` + JSON with the exact order.

3. **Create another user** (Bob) and log in:
   ```bash
   curl -X POST "http://127.0.0.1:8000/auth/register" ^
     -H "Content-Type: application/json" ^
     -d "{\"email\":\"bob@example.com\",\"password\":\"password123\",\"role\":\"user\"}"

   curl -X POST "http://127.0.0.1:8000/auth/login" ^
     -H "Content-Type: application/json" ^
     -d "{\"email\":\"bob@example.com\",\"password\":\"password123\"}"
   ```
   Save token as `%BOB_TOKEN%`.

4. **Get as different user (Bob)** — should be **forbidden**:
   ```bash
   curl "http://127.0.0.1:8000/orders/%ORDER_ID%" ^
     -H "Authorization: Bearer %BOB_TOKEN%"
   ```
   **Expected**: `403 Not authorized to view this order`

5. **Get as admin** — should succeed:
   ```bash
   curl "http://127.0.0.1:8000/orders/%ORDER_ID%" ^
     -H "Authorization: Bearer %ADMIN_TOKEN%"
   ```
   **Expected**: `200`

---

## 6) Transaction Rollback on External Payment Failure

**Create order with failure simulation header**

```bash
curl -X POST "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -H "x-simulate-payment-failure: 1" ^
  -d "{\"product_id\":\"P999\",\"quantity\":1,\"price\":10.0}"
```

**Expected**
- Status code = `400`
- Body: `{"error":"Payment processing failed, transaction rolled back"}`
- **No** new order persisted

**Verify no persistence**
```bash
curl "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%"
```
- The count should remain unchanged from §4.1.

---

## 7) Validation Errors (Schema Guards)

### 7.1 Quantity must be ≥ 1
```bash
curl -X POST "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"product_id\":\"P1\",\"quantity\":0,\"price\":100.0}"
```
**Expected**: `422` with details mentioning `quantity` >= 1.

### 7.2 Price must be > 0
```bash
curl -X POST "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -D - ^
  -d "{\"product_id\":\"P1\",\"quantity\":1,\"price\":0}"
```
**Expected**: `422` with details mentioning `price` > 0.

### 7.3 product_id must be non-empty
```bash
curl -X POST "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer %USER_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"product_id\":\"\",\"quantity\":1,\"price\":99}"
```
**Expected**: `422` with details for `product_id` min_length(1).

---

## 8) Invalid / Missing Tokens

### 8.1 Missing token
```bash
curl "http://127.0.0.1:8000/orders"
```
**Expected**: `403` (Not authenticated)

### 8.2 Tampered token
```bash
curl "http://127.0.0.1:8000/orders" ^
  -H "Authorization: Bearer not-a-real-token"
```
**Expected**: `401 Invalid token`

---

## 9) Optional: Quick checks via Swagger UI

- Visit `http://127.0.0.1:8000/docs`
- Click **Authorize** (top-right), enter `Bearer <token>`
- Exercise: `POST /orders`, `GET /orders`, `GET /orders/{order_id}`
- Check results match the expectations above.

---

## 10) Verification Checklist (tick as you go)

- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] Register admin & user (201)
- [ ] Login admin & user (200) → tokens captured
- [ ] Orders without token → 403
- [ ] Create order success (201, `status=confirmed`)
- [ ] Notification line written to `notifications.log`
- [ ] User list shows only user’s orders
- [ ] Admin list shows all orders
- [ ] Owner can GET order by id (200)
- [ ] Other user cannot GET order by id (403)
- [ ] Admin can GET order by id (200)
- [ ] Simulated payment failure → 400, **no** persistence
- [ ] Validation errors return `422` with field details
- [ ] Invalid token → 401

---

## 11) Troubleshooting

- **Windows file lock**: Stop the server before deleting `app.db` or `notifications.log`. If needed, wait 100–200ms for background tasks to flush.
- **401/403 confusion**: Missing token → 403 from the auth scheme; present but bad token → 401 (invalid/expired).
- **No notification**: Ensure server continues running after the request; background task appends to `notifications.log`.
- **Env overrides**: You can set `SECRET_KEY` and `DATABASE_URL` to customize the environment.

---

**End of Guide** — This sequence covers the full happy‑path, RBAC rules, async behavior, validation, and failure‑rollback logic.
