import unittest
from decimal import Decimal
from datetime import datetime
from bank_oop.money import Money
from bank_oop.accounts import SavingsAccount, CheckingAccount
from bank_oop.exceptions import InsufficientFundsError

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.opening = Money(Decimal("100.00"))
        self.sav = SavingsAccount("S1", "Asha", self.opening, interest_rate=6.0)
        self.chk = CheckingAccount("C1", "Raj", self.opening, overdraft_limit=Money(Decimal("50.00")))

    def test_deposit_withdraw(self):
        self.sav.deposit(Money(Decimal("50.00")))
        self.assertEqual(self.sav.balance.amount, Decimal("150.00"))
        self.sav.withdraw(Money(Decimal("25.00")))
        self.assertEqual(self.sav.balance.amount, Decimal("125.00"))

    def test_overdraft(self):
        self.chk.withdraw(Money(Decimal("120.00")))
        self.assertEqual(self.chk.balance.amount, Decimal("-20.00"))
        with self.assertRaises(InsufficientFundsError):
            self.chk.withdraw(Money(Decimal("40.01")))

    def test_len_transactions(self):
        self.sav.deposit(Money(Decimal("1.00")))
        self.sav.withdraw(Money(Decimal("1.00")))
        self.assertEqual(len(self.sav), 3)  # opening + 2 ops

    def test_interest(self):
        self.sav.apply_interest()
        # Monthly interest on 100 at 6% p.a. = 0.5
        self.assertEqual(self.sav.balance.amount, Decimal("100.50"))
