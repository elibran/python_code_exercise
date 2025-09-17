"""
KISS_Complined.py
COMPLIANT: Simple, direct, and Pythonic
"""
def calculate_withdrawal_fee(balance: float) -> float:
    """Calculates a $5 withdrawal fee if the balance is below $500."""
    if balance < 500:
        return 5.0
    return 0.0

# An even more concise "one-liner" version
def calculate_withdrawal_fee_oneline(balance: float) -> float:
    """Calculates a $5 withdrawal fee if the balance is below $500."""
    return 5.0 if balance < 500 else 0.0


if __name__ == "__main__":
    print("Compliant (balance 400) =>", calculate_withdrawal_fee(400))
    print("Compliant (balance 600) =>", calculate_withdrawal_fee(600))
    print("Compliant oneline (balance 400) =>", calculate_withdrawal_fee_oneline(400))
    print("Compliant oneline (balance 600) =>", calculate_withdrawal_fee_oneline(600))
