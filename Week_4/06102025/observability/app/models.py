from pydantic import BaseModel, Field # type: ignore

class TransferRequest(BaseModel):
    userId: str = Field(..., description="User ID")
    fromAccount: str
    toAccount: str
    amount: float

class LoginRequest(BaseModel):
    username: str
    password: str
