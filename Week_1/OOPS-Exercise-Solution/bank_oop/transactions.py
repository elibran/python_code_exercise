from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .money import Money

@dataclass(frozen=True, slots=True)
class Transaction:
    """Immutable record of a balance change."""
    amount: Money
    timestamp: datetime
    description: str = ""

    # Frozen dataclass makes this hashable; default __repr__ is descriptive.
