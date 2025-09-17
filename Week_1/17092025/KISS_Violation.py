"""
KISS_Violation.py
VIOLATION: Overly complex for a simple binary choice
"""
def calculate_withdrawal_fee(balance: float, withdrawal_amount: float) -> float:
    fee_status = "NO_FEE"

    if withdrawal_amount > 0:
        if balance < 500:
            fee_status = "APPLY_FEE"

    # Using a dictionary as a switch is overkill here
    fee_map = {
        "APPLY_FEE": 5.0,
        "NO_FEE": 0.0
    }

    return fee_map.get(fee_status, 0.0)


if __name__ == "__main__":
    print("Violation (balance 400, withdrawal 100) =>", calculate_withdrawal_fee(400, 100))
    print("Violation (balance 600, withdrawal 100) =>", calculate_withdrawal_fee(600, 100))
