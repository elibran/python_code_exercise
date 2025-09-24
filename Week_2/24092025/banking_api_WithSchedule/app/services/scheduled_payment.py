from sqlalchemy.orm import Session
from app.repositories import scheduled_payment as repo
from app.schemas.scheduled_payment import ScheduledPaymentCreate

def get_scheduled_payments(db: Session, account_id: int):
    return repo.get_by_account(db, account_id)

def create_scheduled_payment(db: Session, account_id: int, payment: ScheduledPaymentCreate):
    return repo.create(db, account_id, payment)

def delete_scheduled_payment(db: Session, payment_id: int):
    return repo.delete(db, payment_id)
