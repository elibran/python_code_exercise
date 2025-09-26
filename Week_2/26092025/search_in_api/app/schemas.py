from pydantic import BaseModel, field_validator # pyright: ignore[reportMissingImports]

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


class SearchByNameRequest(BaseModel):
    name: str
    limit: int = 50

    @field_validator('name')
    @classmethod
    def _name_nonempty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        if len(v) > 64:
            raise ValueError("name too long (max 64).")
        return v

    @field_validator('limit')
    @classmethod
    def _limit_range(cls, v: int) -> int:
        if v <= 0 or v > 200:
            raise ValueError("limit must be between 1 and 200.")
        return v

class SearchResult(BaseModel):
    account: str
    customer_name: str
    balance: float
    account_type: str
