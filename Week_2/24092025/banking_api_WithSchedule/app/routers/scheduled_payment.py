from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import scheduled_payment as service
from app.schemas.scheduled_payment import ScheduledPaymentCreate, ScheduledPaymentResponse
from typing import List

router = APIRouter()

@router.get("/accounts/{account_id}/scheduled-payments", response_model=List[ScheduledPaymentResponse])
def list_scheduled_payments(account_id: int, db: Session = Depends(get_db)):
    return service.get_scheduled_payments(db, account_id)

@router.post("/accounts/{account_id}/scheduled-payments", response_model=ScheduledPaymentResponse)
def create_scheduled_payment(account_id: int, payment: ScheduledPaymentCreate, db: Session = Depends(get_db)):
    return service.create_scheduled_payment(db, account_id, payment)

@router.delete("/scheduled-payments/{payment_id}")
def delete_scheduled_payment(payment_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_scheduled_payment(db, payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scheduled payment not found")
    return {"message": "Scheduled payment deleted successfully"}
