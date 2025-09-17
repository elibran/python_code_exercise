"""
LSP_Complied.py
Refactors so only withdraw-capable accounts expose withdraw().
"""
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, balance: float = 0.0) -> None:
        self._balance = balance
    def deposit(self, amount: float) -> None:
        self._balance += amount
    @property
    def balance(self) -> float:
        return self._balance

class Withdrawable(ABC):
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        ...

class SavingsAccount(Account, Withdrawable):
    def withdraw(self, amount: float) -> None:
        if self._balance < amount:
            raise ValueError("Insufficient funds")
        self._balance -= amount

class FixedTermDepositAccount(Account):
    # No withdraw() — not withdrawable until maturity
    pass

def withdraw_if_possible(obj, amount: float) -> None:
    if isinstance(obj, Withdrawable):
        obj.withdraw(amount)
    else:
        print(f"Not withdrawable type: {obj.__class__.__name__}")

if __name__ == "__main__":
    savings = SavingsAccount()
    savings.deposit(300)
    withdraw_if_possible(savings, 120)  # OK

    fixed = FixedTermDepositAccount()
    fixed.deposit(1000)
    withdraw_if_possible(fixed, 100)    # Gracefully skipped

    print("Balances -> savings:", savings.balance, "| fixed:", fixed.balance)
