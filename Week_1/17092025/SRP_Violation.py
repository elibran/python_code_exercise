"""
SRP_Violation.py — mirrors Java violation with camelCase names.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class BankAccount:
    accountNumber: str
    customerName: str
    balance: float = 0.0
    _transactions: List[str] = field(default_factory=list)

    # --- Responsibility 1: Core Account Logic (Correct) ---
    def deposit(self, amount: float) -> None:
        self.balance += amount
        self._transactions.append(f"{datetime.now():%Y-%m-%d %H:%M} +{amount:.2f} -> {self.balance:.2f}")

    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        self._transactions.append(f"{datetime.now():%Y-%m-%d %H:%M} -{amount:.2f} -> {self.balance:.2f}")

    # --- SRP VIOLATION 1: Persistence Logic ---
    def saveToDatabase(self) -> None:  # stub for parity with Java
        pass

    def loadFromDatabase(self) -> None:
        pass

    # --- 2: Notification Logic ---
    def sendEmailNotification(self) -> None:
        pass

    # --- SRP VIOLATION 3: Presentation/Reporting Logic ---
    def generateStatement(self) -> str:
        lines = [f"Statement for {self.customerName} ({self.accountNumber})",
                 "-" * 42]
        lines.extend(self._transactions)
        lines.append("-" * 42)
        lines.append(f"Current balance: {self.balance:.2f}")
        return "\n".join(lines)

if __name__ == "__main__":
    acct = BankAccount(accountNumber="AC-1001", customerName="Abinash")
    acct.deposit(200)
    acct.withdraw(50)
    print(acct.generateStatement())
    acct.saveToDatabase()
    acct.sendEmailNotification()
