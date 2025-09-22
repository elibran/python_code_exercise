import unittest
from decimal import Decimal
from bank_oop.bank import Bank
from bank_oop.money import Money
from bank_oop.accounts import SavingsAccount, CheckingAccount
from bank_oop.strategies import SimpleInterestStrategy

class TestBank(unittest.TestCase):
    def test_add_and_total(self):
        bank = Bank.create_default()
        bank.add_account(SavingsAccount("S1","Abinash", Money(Decimal("100.00")), interest_rate=6.0))
        bank.add_account(CheckingAccount("C1","Rahul", Money(Decimal("50.00")), overdraft_limit=Money(Decimal("20.00"))))
        total = bank.total_assets()
        self.assertEqual(total.amount, Decimal("150.00"))
        self.assertEqual(total.currency, "INR")

    def test_monthly_process(self):
        bank = Bank.create_default()
        s = SavingsAccount("S1","Abinash", Money(Decimal("100.00")), interest_rate=6.0)
        bank.add_account(s)
        bank.monthly_process(SimpleInterestStrategy())
        self.assertEqual(s.balance.amount, Decimal("100.50"))
