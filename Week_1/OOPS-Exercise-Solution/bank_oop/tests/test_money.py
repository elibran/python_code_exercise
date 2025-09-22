import unittest
from decimal import Decimal
from bank_oop.money import Money
from bank_oop.exceptions import CurrencyMismatchError

class TestMoney(unittest.TestCase):
    def test_add_same_currency(self):
        a = Money(Decimal("10.345"), "INR")
        b = Money(Decimal("2.50"), "INR")
        self.assertEqual((a + b).amount, Decimal("12.85"))

    def test_add_diff_currency_raises(self):
        a = Money(Decimal("10.00"), "INR")
        b = Money(Decimal("2.50"), "USD")
        with self.assertRaises(CurrencyMismatchError):
            _ = a + b

    def test_repr_and_str(self):
        m = Money(Decimal("1.20"), "INR")
        self.assertIn("INR", repr(m))
        self.assertIn("1.20", str(m))
