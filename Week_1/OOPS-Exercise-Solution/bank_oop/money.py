from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, getcontext, ROUND_HALF_UP
from functools import total_ordering
from typing import Any
from .exceptions import CurrencyMismatchError
from .utils import quantize_2

getcontext().prec = 28

@total_ordering
@dataclass(frozen=True, slots=True)
class Money:
    """Represents money with currency using Decimal for precision."""
    amount: Decimal
    currency: str = "INR"

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        object.__setattr__(self, "amount", quantize_2(self.amount))
        if not isinstance(self.currency, str) or not self.currency:
            raise ValueError("currency must be a non-empty string")

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(f"{self.currency} vs {other.currency}")

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.amount == other.amount

    def __lt__(self, other: "Money") -> bool:
        self._check_currency(other)
        return self.amount < other.amount

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency='{self.currency}')"

    def __str__(self) -> str:
        return f"{self.currency} {self.amount}"
