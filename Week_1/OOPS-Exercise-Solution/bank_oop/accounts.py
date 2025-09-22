from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from decimal import Decimal

from .money import Money
from .transactions import Transaction
from .exceptions import InsufficientFundsError, InvalidOperationError, CurrencyMismatchError
from .mixins import JSONSerializable, Auditable

class Account(ABC):
    """Abstract base account with encapsulated balance and ledger."""
    bank_code: str = "FIC"

    def __init__(self, id: str, owner: str, opening_balance: Money):
        if opening_balance.amount < 0:
            raise InvalidOperationError("Opening balance cannot be negative")
        self._id = id
        self._owner = owner
        self._balance: Money = opening_balance
        self._ledger: List[Transaction] = [Transaction(opening_balance, datetime.utcnow(), "opening_balance")]

    @property
    def id(self) -> str:
        return self._id

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def balance(self) -> Money:
        return self._balance

    @abstractmethod
    def account_type(self) -> str:
        ...

    def _append_txn(self, amount: Money, description: str) -> None:
        self._ledger.append(Transaction(amount, datetime.utcnow(), description))

    def deposit(self, money: Money) -> None:
        if money.amount <= 0:
            raise InvalidOperationError("Deposit amount must be positive")
        if money.currency != self._balance.currency:
            raise CurrencyMismatchError("Currency mismatch in deposit")
        self._balance = self._balance + money
        self._append_txn(money, "deposit")
        if hasattr(self, "_touch"):
            self._touch()  # type: ignore[attr-defined]

    def withdraw(self, money: Money) -> None:
        if money.amount <= 0:
            raise InvalidOperationError("Withdraw amount must be positive")
        if money.currency != self._balance.currency:
            raise CurrencyMismatchError("Currency mismatch in withdraw")
        if self._balance.amount < money.amount:
            raise InsufficientFundsError("Insufficient funds")
        self._balance = self._balance - money
        self._append_txn(Money(-money.amount, money.currency), "withdraw")
        if hasattr(self, "_touch"):
            self._touch()  # type: ignore[attr-defined]

    def transfer(self, to: "Account", money: Money) -> None:
        if to is self:
            raise InvalidOperationError("Cannot transfer to the same account")
        # Withdraw first; if it fails, nothing is changed.
        self.withdraw(money)
        try:
            to.deposit(money)
        except Exception as e:
            # rollback to maintain atomicity
            self.deposit(money)
            raise

    def __len__(self) -> int:
        return len(self._ledger)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id} owner={self._owner} balance={self._balance}>"

class InterestBearingAccount(Account, ABC):
    @abstractmethod
    def apply_interest(self) -> None:
        ...

class SavingsAccount(InterestBearingAccount, JSONSerializable, Auditable):
    def __init__(self, id: str, owner: str, opening_balance: Money, interest_rate: float):
        self.interest_rate = Decimal(str(interest_rate))  # ensure Decimal, not float
        super().__init__(id, owner, opening_balance)
        Auditable.__init__(self)

    def account_type(self) -> str:
        return "savings"

    def apply_interest(self) -> None:
        # monthly pro-rated interest as Decimal
        monthly_rate = (self.interest_rate / Decimal("12")) / Decimal("100")
        inc = Money(self.balance.amount * monthly_rate, self.balance.currency)
        if inc.amount > 0:
            self._balance = self._balance + inc
            self._append_txn(inc, "interest")
            self._touch()

class CheckingAccount(Account):
    def __init__(self, id: str, owner: str, opening_balance: Money, overdraft_limit: Money):
        self.overdraft_limit = overdraft_limit
        super().__init__(id, owner, opening_balance)

    def account_type(self) -> str:
        return "checking"

    def withdraw(self, money: Money) -> None:
        if money.amount <= 0:
            raise InvalidOperationError("Withdraw amount must be positive")
        if money.currency != self.balance.currency:
            raise CurrencyMismatchError("Currency mismatch in withdraw")
        projected = self.balance.amount - money.amount
        if projected < -self.overdraft_limit.amount:
            raise InsufficientFundsError("Overdraft limit exceeded")
        self._balance = self._balance - money
        self._append_txn(Money(-money.amount, money.currency), "withdraw")
