# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict # type: ignore

class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=3, max_length=30)
    email: EmailStr

class AccountCreate(AccountBase):
    id: int

class AccountUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    type: str | None = Field(None, min_length=3, max_length=30)
    email: EmailStr | None = None

class AccountOut(AccountBase):
    id: int
    # Pydantic v2 equivalent of `class Config: from_attributes = True`
    model_config = ConfigDict(from_attributes=True)
