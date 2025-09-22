from __future__ import annotations
from typing import Dict
from .accounts import Account
from .money import Money
from .exceptions import AccountNotFoundError, InvalidOperationError, CurrencyMismatchError

class Bank:
    def __init__(self, currency: str = "INR"):
        self._accounts: Dict[str, Account] = {}
        self._currency = currency

    @classmethod
    def create_default(cls) -> "Bank":
        return cls()

    def add_account(self, account: Account) -> None:
        if account.id in self._accounts:
            raise InvalidOperationError(f"Duplicate account id: {account.id}")
        if account.balance.currency != self._currency:
            raise CurrencyMismatchError("Bank currency mismatch with account")
        self._accounts[account.id] = account

    def get(self, account_id: str) -> Account:
        try:
            return self._accounts[account_id]
        except KeyError as e:
            raise AccountNotFoundError(account_id) from e

    def monthly_process(self, strategy) -> None:
        for acct in self._accounts.values():
            if hasattr(strategy, "apply_month_end"):
                strategy.apply_month_end(acct)

    def total_assets(self) -> Money:
        total = sum((a.balance.amount for a in self._accounts.values()), start=Money(0, self._currency).amount)
        return Money(total, self._currency)
