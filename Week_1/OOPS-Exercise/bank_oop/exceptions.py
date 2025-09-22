class BankError(Exception):
    """Base class for all bank-related exceptions."""

class CurrencyMismatchError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass

class InvalidOperationError(BankError):
    pass
