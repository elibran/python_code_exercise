"""
ISP_Violation.py
"""
from typing import Protocol

class BankingOperations(Protocol):
    def check_balance(self, account_id: str) -> None: ...
    def make_deposit(self, account_id: str, amount: float) -> None: ...
    def make_withdrawal(self, account_id: str, amount: float) -> None: ...
    def open_new_account(self, customer_name: str) -> None: ...
    def close_account(self, account_id: str) -> None: ...

class AccountHolder(BankingOperations):
    def check_balance(self, account_id: str) -> None:
        print("Checking balance...")
    def make_deposit(self, account_id: str, amount: float) -> None:
        print("Depositing...")
    def make_withdrawal(self, account_id: str, amount: float) -> None:
        print("Withdrawing...")
    def open_new_account(self, customer_name: str) -> None:
        raise NotImplementedError("Account holders cannot open new accounts.")
    def close_account(self, account_id: str) -> None:
        raise NotImplementedError("Account holders cannot close accounts.")
