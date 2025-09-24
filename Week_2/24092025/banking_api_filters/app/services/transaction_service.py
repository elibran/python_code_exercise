from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..repositories.transaction_repository import list_by_account
from ..models.transaction import Transaction

class TransactionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def list_transactions(
        self,
        account_id: int,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: int = 1,
        limit: int = 25,
    ) -> List[Transaction]:
        return list_by_account(self.db, account_id, status, sort_by, page, limit)
