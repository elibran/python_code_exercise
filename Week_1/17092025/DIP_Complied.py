"""
DIP_Complined.py
DIP-compliant — TransactionService depends on a Notifier abstraction.
"""
from typing import Protocol
import time
from datetime import datetime

# Step 1: Abstraction (contract)
class Notifier(Protocol):
    def send(self, message: str) -> None: ...

# Step 2: Low-level modules conform to the abstraction
class EmailNotifier:
    def send(self, message: str) -> None:
        time.sleep(5)
        print(f"Sending email notification: {message}")

class SmsNotifier:
    def send(self, message: str) -> None:
        print(f"Sending SMS notification: {message}")

# Step 3: High-level module depends only on abstraction
class TransactionService:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier  # injected dependency

    def completeTransaction(self, amount: float) -> None:
        # ... transaction logic ...
        print(f"Transaction of ${amount} completed.")
        self.notifier.send(f"Transaction of ${amount} was successful.")
        print(f"End: {datetime.now()}")


if __name__ == "__main__":
    print(f"Start: {datetime.now()}")

    emailSvc = TransactionService(EmailNotifier())
    emailSvc.completeTransaction(100.0)

    smsSvc = TransactionService(SmsNotifier())
    smsSvc.completeTransaction(250.0)
