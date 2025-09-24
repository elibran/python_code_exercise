from pydantic import BaseModel # type: ignore
from datetime import datetime

class TransactionOut(BaseModel):
    id: int
    account_id: int
    amount: float
    status: str
    date: datetime
    description: str | None = None

    class Config:
        orm_mode = True
