from typing import List
from fastapi import APIRouter, Depends, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from ..services.account_service import AccountService
from ..schemas.account_schema import AccountCreate, AccountOut, TransferRequest, KYCStatusOut, KYCStatusUpdate

from typing import Optional
router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountOut)
def create_account(account_data: AccountCreate, service: AccountService = Depends()):
    return service.create_account(account_data)

@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, service: AccountService = Depends()):
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/", response_model=List[AccountOut])
def get_all_accounts(service: AccountService = Depends()):
    return service.get_all_accounts()

class AmountRequest(BaseModel):
    amount: float

@router.post("/{account_id}/deposit", response_model=AccountOut)
def deposit_money(account_id: int, request: AmountRequest, service: AccountService = Depends()):
    try:
        updated_account = service.deposit(account_id, request.amount)
        if not updated_account:
            raise HTTPException(status_code=404, detail="Account not found")
        return updated_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{account_id}/withdraw", response_model=AccountOut)
def withdraw_money(account_id: int, request: AmountRequest, service: AccountService = Depends()):
    try:
        updated_account = service.withdraw(account_id, request.amount)
        if not updated_account:
            raise HTTPException(status_code=404, detail="Account not found")
        return updated_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transfer", response_model=List[AccountOut])
def transfer_money(request: TransferRequest, service: AccountService = Depends()):
    try:
        from_acct, to_acct = service.transfer(request.from_account_id, request.to_account_id, request.amount)
        return [from_acct, to_acct]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{account_id}/kyc-status", response_model=KYCStatusOut)
def get_kyc_status(account_id: int, service: AccountService = Depends()):
    status = service.is_kyc_compliant(account_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return KYCStatusOut(account_id=account_id, kyc_compliant=status)

@router.put("/{account_id}/kyc-status", response_model=KYCStatusOut)
def set_kyc_status(
    account_id: int,
    payload: Optional[KYCStatusUpdate] = None,
    kyc_compliant: Optional[bool] = None,
    service: AccountService = Depends(),
):
    """Idempotently set an account's KYC status."""
    new_value = (
        payload.kyc_compliant if payload is not None
        else kyc_compliant if kyc_compliant is not None
        else True
    )
    acct = service.set_kyc_compliant(account_id, new_value)
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    return KYCStatusOut(account_id=acct.id, kyc_compliant=acct.kyc_compliant)

from fastapi import Query # type: ignore
from ..services.transaction_service import TransactionService
from ..schemas.transaction_schema import TransactionOut

@router.get("/{account_id}/transactions", response_model=List[TransactionOut])
def list_transactions(
    account_id: int,
    status: str | None = Query(default=None, description="Filter by status, e.g., completed"),
    sortBy: str | None = Query(default=None, description="Sort by 'field:direction', e.g., date:desc"),
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    limit: int = Query(default=25, ge=1, le=100, description="Page size; default 25; max 100"),
    service: TransactionService = Depends(),
):
    """Return transactions for an account with optional filtering, sorting, and pagination.
    - status: filter by transaction status (e.g., completed, pending, failed)
    - sortBy: sort by 'date', 'amount', 'id', or 'status' with ':asc' or ':desc'
    - page/limit: pagination with sensible defaults and max limit cap
    """
    return service.list_transactions(
        account_id=account_id,
        status=status,
        sort_by=sortBy,
        page=page,
        limit=limit,
    )
