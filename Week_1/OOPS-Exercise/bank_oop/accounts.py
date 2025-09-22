from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from .money import Money
from .transactions import Transaction
from .exceptions import InsufficientFundsError, InvalidOperationError
from .mixins import JSONSerializable, Auditable
from datetime import datetime

class Account(ABC):
    bank_code: str = "FIC"

    def __init__(self, id: str, owner: str, opening_balance: Money):
        # TODO: encapsulate balance (private) and maintain a ledger list
        pass

    @property
    def balance(self) -> Money:
        # TODO: return current balance (read-only property)
        raise NotImplementedError

    @abstractmethod
    def account_type(self) -> str:
        ...

    def deposit(self, money: Money) -> None:
        # TODO: validate positive amount and currency; append Transaction
        raise NotImplementedError

    def withdraw(self, money: Money) -> None:
        # TODO: enforce policy, raise InsufficientFundsError when needed
        raise NotImplementedError

    def transfer(self, to: "Account", money: Money) -> None:
        # TODO: withdraw then deposit; ensure currency & atomicity
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO: number of transactions
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self._id} owner={self._owner} balance={self._balance}>"

class InterestBearingAccount(Account, ABC):
    @abstractmethod
    def apply_interest(self) -> None:
        ...

class SavingsAccount(InterestBearingAccount, JSONSerializable, Auditable):
    def __init__(self, id: str, owner: str, opening_balance: Money, interest_rate: float):
        # TODO: store interest_rate; call super().__init__
        pass

    def account_type(self) -> str:
        return "savings"

    def apply_interest(self) -> None:
        # TODO: apply monthly pro-rated interest to balance and record a Transaction
        raise NotImplementedError

class CheckingAccount(Account):
    def __init__(self, id: str, owner: str, opening_balance: Money, overdraft_limit: Money):
        # TODO: store overdraft_limit; call super().__init__
        pass

    def account_type(self) -> str:
        return "checking"

    def withdraw(self, money: Money) -> None:
        # TODO: allow going negative up to overdraft_limit
        raise NotImplementedError
