from pydantic import BaseModel, Field, EmailStr, ConfigDict # type: ignore
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

# --------- Auth ---------
class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.user

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: RoleEnum

# --------- Orders ---------
class OrderCreate(BaseModel):
    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    price: float = Field(..., gt=0)

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    product_id: str
    quantity: int
    price: float
    status: str
