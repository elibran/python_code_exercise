"""
SRP_Complined.py — mirrors Java compliant structure with camelCase names.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Protocol

# --- Core domain model ---
@dataclass
class BankAccount:
    accountNumber: str
    customerName: str
    balance: float = 0.0
    _transactions: List[str] = field(default_factory=list)

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self._transactions.append(f"{datetime.now():%Y-%m-%d %H:%M} +{amount:.2f} -> {self.balance:.2f}")

    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        self._transactions.append(f"{datetime.now():%Y-%m-%d %H:%M} -{amount:.2f} -> {self.balance:.2f}")

    def getTransactions(self) -> List[str]:
        return list(self._transactions)

# --- Presentation ---
class StatementPrinter(Protocol):
    def format(self, account: BankAccount) -> str: ...

class TextStatementPrinter:
    def format(self, account: BankAccount) -> str:
        lines = [f"Statement for {account.customerName} ({account.accountNumber})",
                 "-" * 42]
        lines.extend(account.getTransactions())
        lines.append("-" * 42)
        lines.append(f"Current balance: {account.balance:.2f}")
        return "\n".join(lines)

# --- Persistence ---
class AccountRepository(Protocol):
    def saveToDatabase(self, account: BankAccount) -> None: ...
    def loadFromDatabase(self, account: BankAccount) -> None: ...

class InMemoryAccountRepository:
    def saveToDatabase(self, account: BankAccount) -> None:
        pass
    def loadFromDatabase(self, account: BankAccount) -> None:
        pass

# --- Notification ---
class EmailNotifier(Protocol):
    def sendEmailNotification(self, account: BankAccount) -> None: ...

class ConsoleEmailNotifier:
    def sendEmailNotification(self, account: BankAccount) -> None:
        print(f"Email sent to {account.customerName}")

# --- Service layer ---
class AccountService:
    def __init__(self, printer: StatementPrinter, repository: AccountRepository, notifier: EmailNotifier) -> None:
        self.printer = printer
        self.repository = repository
        self.notifier = notifier

    def printStatement(self, account: BankAccount) -> None:
        print(self.printer.format(account))

    def save(self, account: BankAccount) -> None:
        self.repository.saveToDatabase(account)

    def load(self, account: BankAccount) -> None:
        self.repository.loadFromDatabase(account)

    def notifyEmail(self, account: BankAccount) -> None:
        self.notifier.sendEmailNotification(account)

if __name__ == "__main__":
    acct = BankAccount(accountNumber="AC-2001", customerName="Abinash")
    acct.deposit(500)
    acct.withdraw(120)

    printer = TextStatementPrinter()
    repo = InMemoryAccountRepository()
    notifier = ConsoleEmailNotifier()
    svc = AccountService(printer, repo, notifier)

    svc.printStatement(acct)
    svc.save(acct)
    svc.notifyEmail(acct)
