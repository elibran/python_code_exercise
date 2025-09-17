"""
OCP_Complined.py
Compliant: new account types are added via new classes, calculator stays closed to modification.
"""
from typing import Protocol, Dict

class InterestRule(Protocol):
    def calculate(self, balance: float) -> float: ...

class SavingsInterest:
    def calculate(self, balance: float) -> float: return balance * 0.02

class CheckingInterest:
    def calculate(self, balance: float) -> float: return balance * 0.001

class PremiumInterest:
    def calculate(self, balance: float) -> float: return balance * 0.035

class BusinessInterest:
    def calculate(self, balance: float) -> float: return balance * 0.025

class InterestService:
    def __init__(self) -> None:
        self._rules: Dict[str, InterestRule] = {}
    def registerRule(self, accountType: str, rule: InterestRule) -> None:
        self._rules[accountType] = rule
    def calculateInterest(self, accountType: str, balance: float) -> float:
        rule = self._rules.get(accountType)
        if rule is None:
            raise ValueError(f"Unknown account type: {accountType}")
        return rule.calculate(balance)

if __name__ == "__main__":
    service = InterestService()
    service.registerRule("SAVINGS", SavingsInterest())
    service.registerRule("CHECKING", CheckingInterest())
    service.registerRule("PREMIUM", PremiumInterest())
    print("SAVINGS interest on 1000 =", service.calculateInterest("SAVINGS", 1000))
    print("CHECKING interest on 1000 =", service.calculateInterest("CHECKING", 1000))
    print("PREMIUM interest on 1000 =", service.calculateInterest("PREMIUM", 1000))
    # Add BUSINESS via extension, not by changing the service:
    service.registerRule("BUSINESS", BusinessInterest())
    print("BUSINESS interest on 1000 =", service.calculateInterest("BUSINESS", 1000))
