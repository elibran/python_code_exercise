"""
DIP_Violation.py
Deliberate DIP violation — TransactionService depends directly on EmailNotifier.
"""
import time
from datetime import datetime
class EmailNotifier:
    def sendEmail(self, message: str) -> None:

        time.sleep(5)
        print(f"Sending email notification: {message}")
        # (real email logic would go here)

class TransactionService:
    # High-level module directly creates a concrete dependency (❌)
    def __init__(self) -> None:
        self.emailNotifier = EmailNotifier()  # tight coupling

    def completeTransaction(self, amount: float) -> None:
        # ... transaction logic ...
        print(f"Transaction of ${amount} completed.")
        self.emailNotifier.sendEmail(f"Transaction of ${amount} was successful.")
        print(f"End: {datetime.now()}")


if __name__ == "__main__":
    service = TransactionService()
    print(f"Start: {datetime.now()}")
    service.completeTransaction(125.50)
