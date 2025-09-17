"""
ISP_Complied.py
"""
from typing import Protocol

class AccountHolderActions(Protocol):
    def check_balance(self, account_id: str) -> None: ...
    def make_deposit(self, account_id: str, amount: float) -> None: ...
    def make_withdrawal(self, account_id: str, amount: float) -> None: ...

class BankTellerActions(Protocol):
    def open_new_account(self, customer_name: str) -> None: ...
    def close_account(self, account_id: str) -> None: ...
    def make_deposit(self, account_id: str, amount: float) -> None: ...

class AccountHolder:
    def check_balance(self, account_id: str) -> None:
        print("Checking balance...")
    def make_deposit(self, account_id: str, amount: float) -> None:
        print("Depositing...")
    def make_withdrawal(self, account_id: str, amount: float) -> None:
        print("Withdrawing...")

class BankTeller:
    def check_balance(self, account_id: str) -> None:
        print("Teller is checking balance...")
    def make_deposit(self, account_id: str, amount: float) -> None:
        print("Teller is making a deposit...")
    def make_withdrawal(self, account_id: str, amount: float) -> None:
        print("Teller is processing a withdrawal...")
    def open_new_account(self, customer_name: str) -> None:
        print("Teller is opening an account...")
    def close_account(self, account_id: str) -> None:
        print("Teller is closing an account...")

def perform_customer_actions(client: AccountHolderActions, account_id: str):
    client.check_balance(account_id)
