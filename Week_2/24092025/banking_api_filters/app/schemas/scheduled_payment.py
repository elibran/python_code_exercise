from pydantic import BaseModel # type: ignore
from datetime import datetime

class ScheduledPaymentBase(BaseModel):
    amount: float
    scheduled_date: datetime
    description: str | None = None

class ScheduledPaymentCreate(ScheduledPaymentBase):
    pass

class ScheduledPaymentResponse(ScheduledPaymentBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True
