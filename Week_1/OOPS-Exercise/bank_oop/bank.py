from __future__ import annotations
from typing import Dict, Optional, Iterable
from .accounts import Account, SavingsAccount, CheckingAccount
from .money import Money
from .exceptions import AccountNotFoundError, InvalidOperationError

class Bank:
    def __init__(self, currency: str = "INR"):
        self._accounts: Dict[str, Account] = {}
        self._currency = currency

    @classmethod
    def create_default(cls) -> "Bank":
        return cls()

    def add_account(self, account: Account) -> None:
        # TODO: store by id, prevent duplicates
        raise NotImplementedError

    def get(self, account_id: str) -> Account:
        # TODO: lookup or raise AccountNotFoundError
        raise NotImplementedError

    def monthly_process(self, strategy) -> None:
        # Duck typing: call strategy.apply_month_end(account) if available
        for acct in self._accounts.values():
            if hasattr(strategy, "apply_month_end"):
                strategy.apply_month_end(acct)

    def total_assets(self) -> Money:
        # TODO: sum balances into Money of bank currency
        raise NotImplementedError
