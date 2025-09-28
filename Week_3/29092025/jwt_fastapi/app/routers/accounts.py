from fastapi import APIRouter, Depends # type: ignore
from ..deps import role_required

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/{account_id}")
async def get_account(account_id: str, current=Depends(role_required("customer"))):
    return {"account_id": account_id, "owner": current["username"], "role": current["role"]}

@router.get("/admin/{account_id}")
async def admin_get_account(account_id: str, current=Depends(role_required("admin"))):
    return {"account_id": account_id, "requested_by": current["username"], "role": current["role"]}
