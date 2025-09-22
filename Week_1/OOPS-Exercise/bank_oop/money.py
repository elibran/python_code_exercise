from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Any
from .exceptions import CurrencyMismatchError

getcontext().prec = 28

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = "INR"

    def __post_init__(self):
        # TODO: normalize amount (quantize to 2 places) and validate currency string
        pass

    # TODO: implement __add__, __sub__ (same currency only). Raise CurrencyMismatchError on mismatch.
    # TODO: implement rich comparisons (==, <, <=, >, >=) using amount when currencies match.
    # TODO: implement __repr__ and __str__
