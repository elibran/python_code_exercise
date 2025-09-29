# Full Solution Walkthrough — Beginner Friendly

**Date:** Sep 27, 2025


This guide explains the **solution code** end-to-end for Python freshers. It is self-explanatory, hands-on, and designed to help you connect the dots between **Schemas**, **Models**, **Repositories**, **Services**, and **Routers**.


## Project structure (key files)
```
app/__init__.py
app/__pycache__/__init__.cpython-311.pyc
app/__pycache__/main.cpython-311.pyc
app/api/__init__.py
app/api/__pycache__/__init__.cpython-311.pyc
app/api/v1/__init__.py
app/api/v1/__pycache__/__init__.cpython-311.pyc
app/api/v1/__pycache__/api_router.cpython-311.pyc
app/api/v1/__pycache__/error_handlers.cpython-311.pyc
app/api/v1/api_router.py
app/api/v1/error_handlers.py
app/api/v1/routes/__init__.py
app/api/v1/routes/__pycache__/__init__.cpython-311.pyc
app/api/v1/routes/__pycache__/practitioners.cpython-311.pyc
app/api/v1/routes/__pycache__/slots.cpython-311.pyc
app/api/v1/routes/practitioners.py
app/api/v1/routes/slots.py
app/core/__pycache__/config.cpython-311.pyc
app/core/config.py
app/db/__pycache__/base.cpython-311.pyc
app/db/__pycache__/models.cpython-311.pyc
app/db/__pycache__/repository.cpython-311.pyc
app/db/__pycache__/session.cpython-311.pyc
app/db/base.py
app/db/models.py
app/db/repository.py
app/db/session.py
app/main.py
app/schemas/__pycache__/practitioner.cpython-311.pyc
app/schemas/__pycache__/slot.cpython-311.pyc
app/schemas/practitioner.py
app/schemas/slot.py
app/services/__pycache__/practitioner_service.cpython-311.pyc
app/services/__pycache__/slot_service.cpython-311.pyc
app/services/practitioner_service.py
app/services/slot_service.py
```


## Architecture in one picture
```
Request --> Router (FastAPI) --> Service (business rules) --> Repository (DB operations) --> Model (SQLAlchemy ORM) --> Database
               ^                                                                                                     |
               |------------------------------------------ Schema (Pydantic) ----------------------------------------|
```


## How to run locally
1. Create a virtual environment and install requirements.
2. Start the API:
```
uvicorn app.main:app --reload
```
3. Visit docs at `/docs` (Swagger UI) and `/redoc`.


## Data Model (SQLAlchemy ORM)
The models define how data is stored in the database. Here are the detected models and their columns:


- (Could not parse models automatically; see code below.)


### app/db/models.py
```python
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from .base import Base

class Practitioner(Base):
    __tablename__ = "practitioners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    slots = relationship("Slot", back_populates="practitioner", cascade="all, delete-orphan")

class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioners.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    is_booked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    practitioner = relationship("Practitioner", back_populates="slots")
```


## Schemas (Pydantic v2)
Schemas validate and shape data moving in/out of the API. Detected classes & fields:


**practitioner.py**

- `PractitionerBase` → fields: name, specialty

- `PractitionerRead` → fields: id

**slot.py**

- `SlotBase` → fields: practitioner_id, start_time, end_time, is_booked

- `SlotUpdate` → fields: practitioner_id, start_time, end_time, is_booked

- `SlotRead` → fields: id


### app/schemas/practitioner.py
```python
from pydantic import BaseModel, Field, ConfigDict

class PractitionerBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialty: str = Field(min_length=1, max_length=100)

class PractitionerCreate(PractitionerBase): pass
class PractitionerUpdate(PractitionerBase): pass

class PractitionerRead(PractitionerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```



### app/schemas/slot.py
```python
from datetime import datetime
from pydantic import BaseModel, model_validator, ConfigDict

class SlotBase(BaseModel):
    practitioner_id: int
    start_time: datetime
    end_time: datetime
    is_booked: bool = False

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self

class SlotCreate(SlotBase): pass

class SlotUpdate(BaseModel):
    practitioner_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_booked: bool | None = None

    @model_validator(mode="after")
    def check_times(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self

class SlotRead(SlotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```


## Repository layer (DB helpers)
The repository wraps common CRUD operations so services don't deal with SQLAlchemy details.



### app/db/repository.py
```python
from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)

class Repository(Generic[ModelT]):
    def __init__(self, db: Session, model: Type[ModelT]):
        self.db = db
        self.model = model

    def get(self, id: int):
        return self.db.get(self.model, id)

    def list(self, limit: int = 50, offset: int = 0):
        stmt = select(self.model).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def add(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelT) -> None:
        self.db.delete(obj)
        self.db.commit()

    def update(self) -> None:
        self.db.commit()
```


## Services (business logic)
Services orchestrate repositories, enforce rules, and raise domain errors that routers convert into HTTP responses.


### PractitionerService — responsibilities
- List practitioners with pagination
- Create, read, update, delete practitioners
- Validate inputs at the domain level (beyond Pydantic)



### app/services/practitioner_service.py
```python
from sqlalchemy.orm import Session
from app.db.models import Practitioner
from app.db.repository import Repository
from app.schemas.practitioner import PractitionerCreate, PractitionerUpdate

class PractitionerService:
    def __init__(self, db: Session):
        self.repo = Repository[Practitioner](db, Practitioner)

    def get(self, id: int):
        return self.repo.get(id)

    def list(self, limit: int = 50, offset: int = 0):
        return self.repo.list(limit=limit, offset=offset)

    def create(self, payload: PractitionerCreate):
        obj = Practitioner(name=payload.name, specialty=payload.specialty)
        return self.repo.add(obj)

    def update(self, id: int, payload: PractitionerUpdate):
        obj = self.repo.get(id)
        if not obj:
            return None
        obj.name = payload.name
        obj.specialty = payload.specialty
        self.repo.update()
        return obj

    def delete(self, id: int) -> bool:
        obj = self.repo.get(id)
        if not obj:
            return False
        self.repo.delete(obj)
        return True
```


### SlotService — responsibilities
- List slots with filters (availability, practitioner, date range), sorting, and pagination
- Handle booking logic (already booked → conflict)
- Standard CRUD for slots



### app/services/slot_service.py
```python
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, asc, desc, and_
from app.db.models import Slot
from app.db.repository import Repository
from app.schemas.slot import SlotCreate, SlotUpdate

class SlotService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = Repository[Slot](db, Slot)

    def get(self, id: int):
        return self.repo.get(id)

    def create(self, payload: SlotCreate):
        obj = Slot(
            practitioner_id=payload.practitioner_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
            is_booked=payload.is_booked,
        )
        return self.repo.add(obj)

    def update(self, id: int, payload: SlotUpdate):
        obj = self.repo.get(id)
        if not obj:
            return None
        if payload.practitioner_id is not None:
            obj.practitioner_id = payload.practitioner_id
        if payload.start_time is not None:
            obj.start_time = payload.start_time
        if payload.end_time is not None:
            obj.end_time = payload.end_time
        if payload.is_booked is not None:
            obj.is_booked = payload.is_b
# ... (truncated for brevity in this doc)

```


## Routers (HTTP endpoints)
Routers connect HTTP to services, parse query/body using Schemas, and map domain errors to status codes.


### Detected endpoints


- **GET /{practitioner_id}** → `get_practitioner()` in `routes_prac`

- **PUT /{practitioner_id}** → `update_practitioner()` in `routes_prac`

- **DELETE /{practitioner_id}** → `delete_practitioner()` in `routes_prac`

- **GET /{slot_id}** → `get_slot()` in `routes_slots`

- **PUT /{slot_id}** → `update_slot()` in `routes_slots`

- **DELETE /{slot_id}** → `delete_slot()` in `routes_slots`

- **POST /{slot_id}/book** → `book_slot()` in `routes_slots`


### app/api/v1/routes/practitioners.py
```python
from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.db.session import get_db
from app.schemas.practitioner import PractitionerCreate, PractitionerUpdate, PractitionerRead
from app.services.practitioner_service import PractitionerService

router = APIRouter()

@router.get("", response_model=list[PractitionerRead])
def list_practitioners(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    return PractitionerService(db).list(limit=limit, offset=offset)

@router.post("", response_model=PractitionerRead, status_code=status.HTTP_201_CREATED)
def create_practitioner(payload: PractitionerCreate, db: Session = Depends(get_db)):
    return PractitionerService(db).create(payload)

@router.get("/{practitioner_id}", response_model=PractitionerRead)
def get_practitioner(practitioner_id: int, db: Session = Depends(get_db)):
    obj = PractitionerService(db).get(practitioner_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    return obj

@router.put("/{practitioner_id}", response_model=PractitionerRead)
def update_practitioner(practitioner_id: int
# ... (truncated for brevity in this doc)

```



### app/api/v1/routes/slots.py
```python
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.slot import SlotCreate, SlotUpdate, SlotRead
from app.services.slot_service import SlotService

router = APIRouter()

@router.get("", response_model=list[SlotRead])
def list_slots(
    available: bool | None = None,
    practitioner_id: int | None = None,
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    # keep simple pattern for OpenAPI contract test
    sort_by: str = Query("start_time", pattern="start_time|end_time"),
    order: str = Query("asc", pattern="asc|desc"),
    db: Session = Depends(get_db),
):
    # Runtime guard (pydantic v2 + Query pattern may not validate at runtime)
    if order not in ("asc", "desc"):
        raise HTTPException(status_code=422, detail="Invalid 'order' param; must be 'asc' or 'desc'")

    return SlotService(db).list_filtered(
        available=available,
        practitioner_id=practitioner_id,
        date_from=date_from,
        date_to=date_t
# ... (truncated for brevity in this doc)

```


## Error handling
- `RequestValidationError` → returns 422 with JSON-safe details
- Booking conflicts (already booked) → 409
- Not found → 404



### app/api/v1/error_handlers.py
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

def _json_safe_errors(errs):
    safe = []
    for e in errs:
        e = e.copy()
        ctx = e.get("ctx")
        if isinstance(ctx, dict):
            e["ctx"] = {k: (v if isinstance(v, (str, int, float, bool)) or v is None else str(v)) for k, v in ctx.items()}
        safe.append(e)
    return safe

def init_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": _json_safe_errors(exc.errors())})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
```


## Database session wiring
How SQLAlchemy session/engine is created and injected.



### app/db/session.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from .base import Base

_engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=_engine)
```


## End-to-end walkthroughs

### A) Creating a Practitioner
1. **Router** `POST /api/v1/practitioners` parses body → `PractitionerCreate` schema.
2. **Service** builds ORM object and calls **Repository.add**, then **commit**.
3. **Router** returns `PractitionerOut` with 201 Created.

**Example request**
```bash
curl -X POST http://localhost:8000/api/v1/practitioners   -H "Content-Type: application/json"   -d '{"name": "Dr. Ada", "specialty": "Dermatology"}'
```

### B) Listing Slots with Filters and Sorting
1. **Router** `GET /api/v1/slots` validates query params (e.g., `available`, `practitioner_id`, `date_from`, `date_to`, `sort_by`, `order`, `limit`, `offset`).
2. **Service** constructs a SQL query with conditions and `order_by`, applies `limit`/`offset`.
3. **Router** returns a list of `SlotOut` objects.

**Example request**
```bash
curl "http://localhost:8000/api/v1/slots?available=true&sort_by=start_time&order=asc&limit=20"
```

### C) Booking a Slot
1. **Router** `POST /api/v1/slots/{id}/book` calls `SlotService.book(id)`.
2. **Service** loads the slot; if not found → raise `KeyError` (router → 404).
3. If already booked → raise `ValueError` (router → 409).
4. Else set `is_booked=True`, persist, return updated slot.

**Example request**
```bash
curl -X POST http://localhost:8000/api/v1/slots/1/book
```

Expected outcomes:
- `200 OK` with booked slot
- `404 Not Found` if slot id does not exist
- `409 Conflict` if slot already booked


## Tips & common pitfalls for freshers
- **Always commit** after `add/update/delete` or your changes won't persist.
- **Validate date logic**: ensure `end_time > start_time` (validator in schema).
- **Don't overuse routers for logic**: keep them thin; put rules in services.
- **Prefer repository** over ad-hoc session usage to keep code consistent.
- **Runtime-guard query params** (`order in {"asc","desc"}`) for predictable behavior.
