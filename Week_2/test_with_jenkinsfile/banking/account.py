"""Banking account primitives.

This module exposes a minimal :class:`Account` class with clear, small methods
and explicit errors. The goal is clarity over cleverness.
"""

from __future__ import annotations


class Account:
    """A simple in-memory bank account.

    Parameters
    ----------
    initial_balance : float, optional
        Starting balance for the account. Must be non-negative.
    """

    def __init__(self, initial_balance: float = 0.0) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._balance: float = float(initial_balance)

    def get_balance(self) -> float:
        """Return the current balance as a float."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit a positive ``amount`` into the account.

        Raises
        ------
        ValueError
            If ``amount`` is not strictly positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += float(amount)

    def withdraw(self, amount: float) -> None:
        """Withdraw a positive ``amount`` if funds are available.

        Raises
        ------
        ValueError
            If ``amount`` is not strictly positive, or if funds are insufficient.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= float(amount)
