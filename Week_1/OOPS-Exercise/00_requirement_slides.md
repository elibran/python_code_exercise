# Slides: Understanding the Requirement — Mini Banking & Payments System

## Why this exercise?
- Touches **all pillars of OOP** + **exception handling** in a single coherent domain.
- Forces design trade-offs and API discipline.
- Realistic: money, accounts, transfers, interest, month-end routines.

## What you must build
1. **Core domain:**
   - `Money` (Decimal + currency, operator overloads, equality & ordering)
   - `Transaction` (immutable, hashable)
2. **Account abstraction:**
   - `Account` (abstract) with encapsulated balance & ledger
   - Subclasses: `SavingsAccount`, `CheckingAccount` (+ `InterestBearingAccount` abstract base)
3. **Mixins / Multiple Inheritance:**
   - `JSONSerializable`, `Auditable`
4. **Bank orchestrator & strategies (duck typing):**
   - `Bank.total_assets()`, `Bank.monthly_process(strategy)`
5. **Exceptions:**
   - Custom, specific, meaningful

## Design constraints
- Encapsulation: no public mutation of balances
- Inheritance + composition where it makes sense
- Operator overloading only where it increases clarity
- Robust error handling; avoid bare `except`

## Mandatory dunder methods
- Money: `__add__`, `__sub__`, `__eq__`, ordering, `__repr__`
- Account: `__len__`, `__repr__`
- Transaction: `__hash__`, `__repr__`

## Deliverables to implement
- Working code with docstrings
- All unit tests must pass
- README describing approach and how to run tests

## Hints
- Use `decimal.Decimal` for amounts
- Protect invariants: currencies must match, no negative deposits, overdraft checks
- Use `@property`, `@classmethod`, `@staticmethod` intentionally
