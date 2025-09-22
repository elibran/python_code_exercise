from decimal import Decimal, ROUND_HALF_UP

def quantize_2(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
