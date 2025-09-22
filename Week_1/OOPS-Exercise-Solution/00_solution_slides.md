# Slides: Solution Walkthrough — Mini Banking & Payments System

## Architecture overview
- `money.py`: Money type (Decimal + currency) with operator overloads & validations
- `exceptions.py`: Custom typed exceptions
- `transactions.py`: Immutable, hashable Transaction
- `mixins.py`: JSONSerializable, Auditable
- `accounts.py`: ABC `Account`, `InterestBearingAccount`, `CheckingAccount`, `SavingsAccount`
- `strategies.py`: InterestStrategy (ABC), SimpleInterestStrategy
- `bank.py`: Bank orchestrator with duck-typed month-end processing
- `utils.py`: Helpers (validation, date utilities)

## OOP mapping to requirements
- **Encapsulation**: private balance field, properties only (read-only)
- **Inheritance**: Account → InterestBearingAccount → SavingsAccount; Account → CheckingAccount
- **Multiple inheritance**: SavingsAccount + JSONSerializable + Auditable
- **Polymorphism**: `withdraw`, `apply_interest`, `account_type`
- **Abstraction**: ABCs for Account & Strategy
- **Duck typing**: `monthly_process(strategy)` checks for `apply_month_end` presence

## Exceptions usage
- Specific exceptions with clear messages, raised at the edge of invariants
- Example: currency mismatch, overdraft violation, unknown account
- Use of `raise ... from e` to preserve context

## Magic methods
- `Money` arithmetic & rich comparisons
- `Account.__len__` equals #transactions
- `Transaction.__hash__` enables set usage / dedup

## Testing strategy
- Unit tests per module
- Deterministic fixtures (fixed dates, amounts)
- Behavior-driven assertions: pass on correct OOP semantics

## Complexity & extensibility
- Pluggable strategies for interest and fees
- Mixins decouple concerns (serialization, audit trail)
