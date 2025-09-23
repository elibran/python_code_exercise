from banking.account import Account
import pytest # type: ignore

def test_initial_balance():
    account = Account(100)
    assert account.get_balance() == 100

def test_deposit():
    account = Account(50)
    account.deposit(50)
    assert account.get_balance() == 100

def test_successful_withdrawal():
    account = Account(200)
    account.withdraw(50)
    assert account.get_balance() == 150

def test_withdraw_insufficient_funds():
    account = Account(20)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(50)

def test_withdraw_negative_amount():
    account = Account(100)
    with pytest.raises(ValueError, match="positive"):
        account.withdraw(-10)
