from typing import List, Optional
from fastapi import Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from ..database import get_db
from ..models.account import Account

class AccountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_all(self) -> List[Account]:
        return self.db.query(Account).all()

    def create(self, account: Account) -> Account:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account: Account) -> Account:
        self.db.commit()
        self.db.refresh(account)
        return account

    def transfer_atomic(self, from_id: int, to_id: int, amount: float):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        from_acct = self.get_by_id(from_id)
        to_acct = self.get_by_id(to_id)
        if not from_acct or not to_acct:
            raise ValueError("Source or destination account not found")
        if from_acct.id == to_acct.id:
            raise ValueError("Cannot transfer to the same account")
        if from_acct.balance < amount:
            raise ValueError("Insufficient funds in source account")
        # Perform updates atomically using the same session/commit
        from_acct.balance -= amount
        to_acct.balance += amount
        self.db.add(from_acct); self.db.add(to_acct)
        self.db.commit()
        self.db.refresh(from_acct); self.db.refresh(to_acct)
        return from_acct, to_acct

    def set_kyc_flag(self, account_id: int, value: bool):
        """Update the kyc_compliant flag; returns Account or None if not found."""
        acct = self.get_by_id(account_id)
        if not acct:
            return None
        acct.kyc_compliant = bool(value)
        self.db.add(acct)
        self.db.commit()
        self.db.refresh(acct)
        return acct
