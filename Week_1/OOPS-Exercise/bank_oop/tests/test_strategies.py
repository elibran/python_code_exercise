import unittest
from decimal import Decimal
from bank_oop.money import Money
from bank_oop.accounts import SavingsAccount, CheckingAccount
from bank_oop.strategies import SimpleInterestStrategy

class TestStrategies(unittest.TestCase):
    def test_simple_interest_strategy(self):
        s = SavingsAccount("S1","Asha", Money(Decimal("100.00")), interest_rate=6.0)
        c = CheckingAccount("C1","Raj", Money(Decimal("100.00")), overdraft_limit=Money(Decimal("50.00")))
        strat = SimpleInterestStrategy()
        strat.apply_month_end(s)
        strat.apply_month_end(c)
        # Savings should grow, checking unchanged
        assert s.balance.amount == Decimal("100.50")
        assert c.balance.amount == Decimal("100.00")
