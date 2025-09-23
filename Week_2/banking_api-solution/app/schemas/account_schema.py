from pydantic import BaseModel, ConfigDict, Field # type: ignore

class AccountCreate(BaseModel):
    owner_name: str

class AccountOut(BaseModel):
    id: int
    owner_name: str
    balance: float
    kyc_compliant: bool
    model_config = ConfigDict(from_attributes=True)


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

class KYCStatusOut(BaseModel):
    account_id: int
    kyc_compliant: bool


class KYCStatusUpdate(BaseModel):
    """Request body for updating an account's KYC status.
    Default is True to support the common 'mark compliant' action without a body.
    """
    kyc_compliant: bool = Field(default=True, description="Set to True to mark KYC compliant, False to mark non-compliant")
