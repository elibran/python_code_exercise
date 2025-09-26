from sqlalchemy import Column, Integer, String, Float, ForeignKey # type: ignore
from .database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
