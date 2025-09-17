"""
OCP_Violation.py
Deliberate violation: if/elif chain on accountType inside a single calculator.
"""
class InterestCalculator:
    def calculateInterest(self, accountType: str, balance: float) -> float:
        if accountType == "SAVINGS":
            return balance * 0.02
        elif accountType == "CHECKING":
            return balance * 0.001
        elif accountType == "PREMIUM":
            return balance * 0.035
        # <-- MODIFICATION REQUIRED HERE for new types
        return 0.0

if __name__ == "__main__":
    calc = InterestCalculator()
    print("SAVINGS interest on 1000 =", calc.calculateInterest("SAVINGS", 1000))
    print("CHECKING interest on 1000 =", calc.calculateInterest("CHECKING", 1000))
    print("PREMIUM interest on 1000 =", calc.calculateInterest("PREMIUM", 1000))
