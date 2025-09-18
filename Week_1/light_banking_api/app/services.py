import random
from fastapi import HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore
from . import models, schemas

class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_unique_account_number(self) -> str:
        # Generate ACC + 7 digits; ensure uniqueness
        while True:
            number = f"ACC{random.randint(1000000, 9999999)}"
            exists = (
                self.db.query(models.BankAccount)
                .filter(models.BankAccount.account_number == number)
                .first()
            )
            if not exists:
                return number

    def create_account(self, payload: schemas.AccountCreate) -> models.BankAccount:
        # Must reference an existing customer
        customer = (
            self.db.query(models.Customer)
            .filter(models.Customer.id == payload.customer_id)
            .first()
        )
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {payload.customer_id} not found.",
            )

        entity = models.BankAccount(
            account_type=payload.account_type,
            balance=payload.balance,
            customer_id=payload.customer_id,
            account_number=self._generate_unique_account_number(),
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
