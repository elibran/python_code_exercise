# Mini Banking & Payments — OOP & Exceptions in Python

## How to run tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
Python 3.10+ required. No third-party packages needed.

## Project structure
```
.
├── bank.py
├── accounts.py
├── money.py
├── transactions.py
├── mixins.py
├── strategies.py
├── exceptions.py
├── utils.py
├── README.md
└── tests/
    ├── test_money.py
    ├── test_accounts.py
    ├── test_bank.py
    └── test_strategies.py
```

## Notes
- Monetary arithmetic uses `decimal.Decimal` for precision.
- All exceptions are typed; avoid bare `except`.
- The same tests are provided in the requirements and solution packages.
