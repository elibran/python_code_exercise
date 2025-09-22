from __future__ import annotations
from abc import ABC, abstractmethod
from .accounts import Account, InterestBearingAccount

class InterestStrategy(ABC):
    @abstractmethod
    def apply_month_end(self, account: Account) -> None:
        ...

class SimpleInterestStrategy(InterestStrategy):
    def apply_month_end(self, account: Account) -> None:
        if isinstance(account, InterestBearingAccount):
            account.apply_interest()
