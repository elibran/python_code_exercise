from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Account
from app.schemas import AccountCreate, AccountUpdate, AccountOut
from app.core.email import get_email_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    logger.info("Create account requested id=%s email=%s", payload.id, payload.email)
    if db.get(Account, payload.id) is not None:
        logger.warning("Create failed - duplicate id=%s", payload.id)
        raise HTTPException(status_code=409, detail="Account with this id already exists")
    exists = db.execute(select(Account).where(Account.email == payload.email)).scalar_one_or_none()
    if exists:
        logger.warning("Create failed - duplicate email=%s", payload.email)
        raise HTTPException(status_code=409, detail="Account with this email already exists")

    acct = Account(id=payload.id, name=payload.name, type=payload.type, email=payload.email)
    db.add(acct)
    db.commit()
    db.refresh(acct)

    emailer = get_email_service()
    logger.info("Sending welcome email to %s", acct.email)
    emailer.send(to=acct.email, subject="Welcome", body=f"Hello {acct.name}, your account is created.")

    logger.info("Account created id=%s", acct.id)
    return acct

@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    logger.debug("Fetch account id=%s", account_id)
    acct = db.get(Account, account_id)
    if not acct:
        logger.warning("Account not found id=%s", account_id)
        raise HTTPException(status_code=404, detail="Not found")
    return acct

@router.get("", response_model=List[AccountOut])
def list_accounts(
    type: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="free text filter on name or email"),
    db: Session = Depends(get_db),
):
    logger.debug("List accounts type=%s q=%s", type, q)
    stmt = select(Account)
    if type:
        stmt = stmt.where(Account.type == type)
    if q:
        pattern = f"%{q.lower()}%"
        from sqlalchemy import or_, func
        stmt = stmt.where(or_(func.lower(Account.name).like(pattern), func.lower(Account.email).like(pattern)))
    result = db.execute(stmt).scalars().all()
    logger.info("List accounts returned %d rows", len(result))
    return result

@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, payload: AccountUpdate, db: Session = Depends(get_db)):
    logger.info("Update account id=%s", account_id)
    acct = db.get(Account, account_id)
    if not acct:
        logger.warning("Update failed - not found id=%s", account_id)
        raise HTTPException(status_code=404, detail="Not found")
    if payload.name is not None:
        acct.name = payload.name
    if payload.type is not None:
        acct.type = payload.type
    if payload.email is not None:
        existing = db.execute(select(Account).where(Account.email == payload.email, Account.id != account_id)).scalar_one_or_none()
        if existing:
            logger.warning("Update failed - duplicate email=%s for id=%s", payload.email, account_id)
            raise HTTPException(status_code=409, detail="Another account already uses this email")
        acct.email = payload.email
    db.commit()
    db.refresh(acct)
    logger.info("Update successful id=%s", account_id)
    return acct

@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    logger.info("Delete account id=%s", account_id)
    acct = db.get(Account, account_id)
    if not acct:
        logger.warning("Delete failed - not found id=%s", account_id)
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(acct)
    db.commit()
    logger.info("Delete successful id=%s", account_id)
    return None
