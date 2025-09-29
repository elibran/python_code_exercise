from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore
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
        date_to=date_to,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order,
    )

@router.post("", response_model=SlotRead, status_code=status.HTTP_201_CREATED)
def create_slot(payload: SlotCreate, db: Session = Depends(get_db)):
    return SlotService(db).create(payload)

@router.get("/{slot_id}", response_model=SlotRead)
def get_slot(slot_id: int, db: Session = Depends(get_db)):
    obj = SlotService(db).get(slot_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Slot not found")
    return obj

@router.put("/{slot_id}", response_model=SlotRead)
def update_slot(slot_id: int, payload: SlotUpdate, db: Session = Depends(get_db)):
    svc = SlotService(db)
    obj = svc.get(slot_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Slot not found")
    return svc.update(slot_id, payload)

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(slot_id: int, db: Session = Depends(get_db)):
    svc = SlotService(db)
    ok = svc.delete(slot_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Slot not found")
    return None

@router.post("/{slot_id}/book", response_model=SlotRead)
def book_slot(slot_id: int, db: Session = Depends(get_db)):
    svc = SlotService(db)
    try:
        return svc.book(slot_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
