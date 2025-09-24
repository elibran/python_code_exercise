from sqlalchemy.orm import Session
from app.models.scheduled_payment import ScheduledPayment
from app.schemas.scheduled_payment import ScheduledPaymentCreate

def get_by_account(db: Session, account_id: int):
    return db.query(ScheduledPayment).filter(ScheduledPayment.account_id == account_id).all()

def create(db: Session, account_id: int, payment: ScheduledPaymentCreate):
    db_payment = ScheduledPayment(
        account_id=account_id,
        amount=payment.amount,
        scheduled_date=payment.scheduled_date,
        description=payment.description
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete(db: Session, payment_id: int):
    payment = db.query(ScheduledPayment).filter(ScheduledPayment.id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
        return True
    return False
