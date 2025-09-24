from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey # type: ignore
from sqlalchemy.sql import func # type: ignore
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, index=True)  # e.g., 'completed', 'pending', 'failed'
    date = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    description = Column(String, nullable=True)
