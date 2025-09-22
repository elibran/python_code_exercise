from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from .money import Money

@dataclass(frozen=True, slots=True)
class Transaction:
    amount: Money
    timestamp: datetime
    description: str = ""

    # TODO: ensure hashability (dataclass frozen is ok) and useful __repr__ is auto-generated.
