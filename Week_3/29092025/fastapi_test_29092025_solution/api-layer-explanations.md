# API Layer-by-Layer Explanations (Schema, Model, Repository, Service, Router)

**Date:** Sep 29, 2025

This addendum explains, in plain language, what each architectural layer does for **each API** in this project. Use it as a training handout (no slides required).

---

## Architecture at a glance

- **Schema (Pydantic v2)**: Python classes that validate & serialize data crossing the API boundary (HTTP body, query params, responses). Think of them as *contracts*.
- **Model (SQLAlchemy ORM)**: Python classes that map directly to database tables. Think of them as *storage shapes*.
- **Repository**: Thin, generic data-access functions (CRUD) that operate on ORM models using a DB session.
- **Service**: Business logic orchestration. Validates assumptions, composes repository calls, raises domain errors.
- **Router (FastAPI)**: HTTP endpoints. They parse/validate inputs (via Schemas), call Services, and convert results (or errors) to HTTP responses.

> Rule of thumb: **Routers** do I/O; **Services** do thinking; **Repositories** do DB; **Models** represent tables; **Schemas** represent payloads.

---

# Practitioners API

### 1) Schema (request/response contracts)

- **Where:** `app/schemas/practitioner.py` (typical)
- **Purpose:** Define what the client can send and what the API returns for practitioners.

**Common classes** (names may vary but intent is the same):
- `PractitionerBase`: shared fields (e.g., `name: str`, `specialty: str`)
- `PractitionerCreate(PractitionerBase)`: input for POST (create)
- `PractitionerUpdate`: all fields optional for PUT/PATCH (e.g., `name: str | None`, `specialty: str | None`)
- `PractitionerOut(PractitionerBase)`: output model (includes `id: int`)

**Why we need it:** Ensure inputs are valid (types/required) and responses have a consistent, documented shape. This is how FastAPI generates OpenAPI docs.

---

### 2) Model (database table mapping)

- **Where:** `app/db/models.py`
- **Purpose:** ORM class describing the `practitioners` table.

**Typical columns:**
- `id: int` (primary key, auto-increment)
- `name: str` (indexed for search)
- `specialty: str` (optional index)

**Why we need it:** The ORM model is what SQLAlchemy persists and queries in the database. It is the single source of truth for storage shape.

---

### 3) Repository (DB access helpers)

- **Where:** `app/db/repository.py`
- **Purpose:** Provide small, reusable CRUD helpers for any model; for practitioners we use `Repository[Practitioner]`.

**Typical functions used:**
- `get(id: int) -> Practitioner | None`
- `list(limit: int, offset: int) -> list[Practitioner]`
- `add(entity: Practitioner) -> Practitioner`
- `update(entity: Practitioner) -> Practitioner`
- `delete(entity: Practitioner) -> None`

**Why we need it:** Keeps DB plumbing out of the service logic; easy to mock/stub in unit tests.

---

### 4) Service (business logic)

- **Where:** `app/services/practitioner_service.py`
- **Purpose:** Implement the actual use cases for practitioners. The service uses the repository and decides *how* to handle domain rules and errors.

**Key methods:**
- `get(id)`: fetch or return `None`
- `list(limit, offset)`: pagination
- `create(payload)`: build ORM object from schema, persist, return DTO
- `update(id, payload)`: fetch, apply changes if present, persist
- `delete(id)`: fetch and remove

**Why we need it:** Routes should remain thin. Services isolate rules and make testing straightforward without HTTP concerns.

---

### 5) Router (HTTP endpoints)

- **Where:** `app/api/v1/routes/practitioners.py` (typical)
- **Purpose:** Translate HTTP requests into service calls; translate outcomes to status codes and response schemas.

**Typical endpoints:**
- `GET /api/v1/practitioners?limit&offset` → returns `list[PractitionerOut]`
- `POST /api/v1/practitioners` → body: `PractitionerCreate`, returns `PractitionerOut` (201 Created)
- `GET /api/v1/practitioners/{id}` → returns `PractitionerOut` (404 if not found)
- `PUT /api/v1/practitioners/{id}` → body: `PractitionerUpdate`, returns `PractitionerOut`
- `DELETE /api/v1/practitioners/{id}` → 204 No Content

**Error handling pattern:**
- If not found → `HTTPException(404)`
- Validation errors → FastAPI handles with our Pydantic/exception handler

---

# Slots API

### 1) Schema (request/response contracts)

- **Where:** `app/schemas/slot.py` (typical)
- **Purpose:** Define the shapes for creating, updating, listing, and booking slots.

**Common classes:**
- `SlotBase`: `practitioner_id: int`, `start_time: datetime`, `end_time: datetime`, `is_booked: bool = False`
- `SlotCreate(SlotBase)`: input for POST (create)
- `SlotUpdate`: optional fields for PUT/PATCH
- `SlotOut(SlotBase)`: includes `id: int`
- **Validation:** `end_time` must be **after** `start_time` (model validator raises on violation).

**Why we need it:** Ensure time windows are valid and IDs/types are correct at the API boundary.

---

### 2) Model (database table mapping)

- **Where:** `app/db/models.py`
- **Purpose:** ORM class for the `slots` table with a foreign key to practitioners.

**Typical columns:**
- `id: int` (primary key)
- `practitioner_id: int` (FK to practitioners.id)
- `start_time: datetime`
- `end_time: datetime`
- `is_booked: bool` (default `False`)

**Why we need it:** Reflects how timeslots are stored and related to practitioners.

---

### 3) Repository (DB access helpers)

- **Where:** `app/db/repository.py`
- **Purpose:** Same generic repository used for slots: `Repository[Slot]` providing `get/list/add/update/delete`.

**Why we need it:** Unified CRUD interface across models; less duplicated SQLAlchemy code.

---

### 4) Service (business logic)

- **Where:** `app/services/slot_service.py`
- **Purpose:** Implement operations specific to slots: filtered listing, booking, and standard CRUD.

**Key methods:**
- `get(id)`: `Slot | None`
- `list_filtered(available, practitioner_id, date_from, date_to, limit, offset, sort_by, order)`:
  - Filters: by availability (`is_booked`), practitioner, and date window (`start_time >= date_from`, `end_time <= date_to`)
  - Sorting: `sort_by in ('start_time', 'end_time')` + `order in ('asc', 'desc')`
  - Pagination: `limit/offset`
- `book(id)`:
  - If not found → **raise `KeyError`** (router returns 404)
  - If already booked → **raise `ValueError`** (router returns 409)
  - Else set `is_booked=True` and persist
- CRUD: `create/update/delete` similar to practitioners

**Why we need it:** Encapsulates all domain rules (e.g., booking conflicts) and keeps routers minimal.

---

### 5) Router (HTTP endpoints)

- **Where:** `app/api/v1/routes/slots.py`
- **Purpose:** Define the HTTP interface for slots, parse/validate query params, and map service outcomes to HTTP responses.

**Typical endpoints:**
- `GET /api/v1/slots`
  - Query params: `available`, `practitioner_id`, `date_from`, `date_to`, `sort_by`, `order`, `limit`, `offset`
  - Returns: `list[SlotOut]`
- `POST /api/v1/slots` → body: `SlotCreate`, returns `SlotOut` (201 Created)
- `GET /api/v1/slots/{id}` → returns `SlotOut` (404 if not found)
- `PUT /api/v1/slots/{id}` → body: `SlotUpdate`, returns `SlotOut`
- `DELETE /api/v1/slots/{id}` → 204 No Content
- `POST /api/v1/slots/{id}/book` → returns `SlotOut`
  - Maps `ValueError` → **409 Conflict**
  - Maps `KeyError` → **404 Not Found**

**Validation guard example:**
- Keep `Query(pattern=...)` simple for schema docs, then **runtime-check** values:
  - `if order not in ("asc","desc"): raise HTTPException(422, "...")`

---

## How the layers work together (request lifecycle)

1. **Router** receives HTTP request → parses path/query/body using **Schemas**.
2. **Router** calls a **Service** method with validated values.
3. **Service** uses a **Repository** to talk to the DB through **Models**.
4. **Service** returns success data or raises a domain error (e.g., `ValueError`, `KeyError`).
5. **Router** maps domain errors to HTTP status codes (e.g., 404, 409) and returns a **Schema** response.
6. If Pydantic parsing fails, the **Error Handler** serializes validation errors into safe JSON (`detail`).

> Teaching tip: Have learners trace one endpoint end-to-end (e.g., `POST /slots`) and identify which layer they’re in at each line of code.

---

## Quick checklists for beginners

**When adding a new field (e.g., practitioner phone):**
- Model: add column to ORM class & migration
- Schema: include in `Create`, `Update`, and `Out` types as appropriate
- Service: allow reading/writing this field
- Router: confirm request/response models updated
- Tests: cover create/get/list/update flows

**When adding a new feature (e.g., cancel a booking):**
- Service: add `cancel_book(id)` with rules (only if booked)
- Router: add `POST /slots/{id}/cancel`
- Repository: usually unchanged (reuse `get/update`)
- Schemas: response type likely `SlotOut` reused
- Tests: success + edge cases (not found, not booked)

---

## Error handling patterns to copy

- Validation errors → 422 with JSON-safe `detail`
- Not found (entity) → 404
- Business conflict (already booked, duplicate, etc.) → 409
- Malformed query param (unsupported sort/order) → 422

---

**End of addendum** — Use this handout alongside the main analysis report for fresher training.
