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
def update_practitioner(practitioner_id: int, payload: PractitionerUpdate, db: Session = Depends(get_db)):
    svc = PractitionerService(db)
    obj = svc.get(practitioner_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    return svc.update(practitioner_id, payload)

@router.delete("/{practitioner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_practitioner(practitioner_id: int, db: Session = Depends(get_db)):
    svc = PractitionerService(db)
    ok = svc.delete(practitioner_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Practitioner not found")
    return None
