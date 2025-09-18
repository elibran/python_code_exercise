from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str

class CustomerOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class AccountCreate(BaseModel):
    account_type: str
    balance: float
    customer_id: int

class Account(BaseModel):
    id: int
    account_number: str
    account_type: str
    balance: float
    customer_id: int
    class Config:
        orm_mode = True
