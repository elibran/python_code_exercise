"""
LSP_Violation.py
FixedTermDepositAccount overrides withdraw() to raise, breaking substitutability.
"""
class BankAccount:
    def __init__(self, balance: float = 0.0) -> None:
        self._balance = balance

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if self._balance < amount:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    @property
    def balance(self) -> float:
        return self._balance

class SavingsAccount(BankAccount):
    # Inherits behavior as-is (OK)
    pass

class FixedTermDepositAccount(BankAccount):
    def withdraw(self, amount: float) -> None:
        # ❌ LSP violation: unexpected exception for a core behavior
        raise NotImplementedError("Cannot withdraw from a fixed-term deposit account.")

def process_withdrawal(acct: BankAccount, amount: float) -> None:
    # Expects any BankAccount to support withdraw()
    acct.withdraw(amount)  # Will explode for FixedTermDepositAccount

if __name__ == "__main__":
    savings = SavingsAccount()
    savings.deposit(200)
    process_withdrawal(savings, 50)  # OK

    fixed = FixedTermDepositAccount()
    fixed.deposit(500)
    try:
        process_withdrawal(fixed, 100)  # ❌ NotImplementedError
    except Exception as e:
        print("Caught:", e)
    print("Balances -> savings:", savings.balance, "| fixed:", fixed.balance)
