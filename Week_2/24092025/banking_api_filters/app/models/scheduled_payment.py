from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from app.database import Base

class ScheduledPayment(Base):
    __tablename__ = "scheduled_payments"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
