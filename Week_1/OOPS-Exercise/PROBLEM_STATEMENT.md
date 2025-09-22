# Exercise: Design a Mini Banking & Payments System (Python OOP + Exceptions)

## Goal
Build a **mini banking system** that demonstrates deep understanding of **OOP in Python** and **robust exception handling**.

You will implement:
- Core domain classes (`Money`, `Transaction`, `Account` hierarchy) using **encapsulation**, **inheritance**, **polymorphism**, and **abstraction**.
- **Operator overloading** (`__add__`, `__sub__`, `__eq__`, `__repr__`, etc.) where appropriate.
- **Mixins & multiple inheritance** for reusable capabilities (e.g., serialization, audit trail).
- **Class methods**, **static methods**, and **properties**.
- **Duck typing** (e.g., a `monthly_process(strategy)` that accepts any object with `apply_month_end(account)`).
- **Clean error handling** with custom exceptions and best practices.
- A small **Bank** orchestrator to create accounts, transfer money, and run month-end processing.
- **Unit tests** must pass in full.

Complexity is **medium–high**; aim for correctness, clarity, and idiomatic Python.

---

## Functional Requirements

### 1. Money
- Represents an amount using `decimal.Decimal` and a `currency` (e.g., `"INR"`).
- Supports arithmetic with **same-currency** only:
  - `+` and `-` between `Money` values.
  - Comparisons (`==`, `<`, `<=`, `>`, `>=`).
- String forms via `__str__` and `__repr__`.
- Raises `CurrencyMismatchError` for cross-currency arithmetic.

### 2. Transaction
- Immutable record of a balance change: `amount: Money`, `timestamp`, `description`.
- Should be **hashable** and printable.

### 3. Account (Abstract)
- Fields: `id` (string), `owner` (string), **encapsulated** balance, and a **ledger** of transactions.
- Methods:
  - `deposit(money: Money) -> None`
  - `withdraw(money: Money) -> None` (raise `InsufficientFundsError` as needed)
  - `transfer(to: "Account", money: Money) -> None`
  - `balance` property (read-only), `__len__` (#transactions), and `__repr__`.
- **Encapsulation**: disallow direct external mutation of balance, use properties.
- **Abstraction**: subclass specialization must implement `account_type()` and may override policies.

### 4. Account Types (Inheritance)
- `InterestBearingAccount` → abstract class with `apply_interest()` to be called during month-end.
- `SavingsAccount(InterestBearingAccount)` → has an `interest_rate` (e.g., 3–7% p.a., apply monthly pro‑rated).
- `CheckingAccount(Account)` → has an `overdraft_limit` allowing negative balances up to the limit.
- Demonstrate **method overriding** and `super()` usage.
- Add a **mixin** (e.g., `JSONSerializable`) to at least one account type to show **multiple inheritance**.

### 5. Bank Orchestrator
- Creates accounts with a factory **class method** (`Bank.from_config` or `Bank.create_*`).
- Looks up accounts by id, processes **month-end** using a **duck‑typed** `strategy`:
  - `strategy.apply_month_end(account)` called for each account if the strategy provides it.
- Provides `total_assets()` returning a `Money` sum across accounts.

### 6. Strategies (Abstraction & Duck Typing)
- Define an `InterestStrategy` **ABC** with `apply_month_end(account)`.
- Provide at least one concrete strategy (e.g., `SimpleInterestStrategy`) that calls `apply_interest()` where applicable.

### 7. Mixins
- `JSONSerializable` → provides `to_json()` and `from_json()` (class method) using only public API.
- `Auditable` → adds `created_at` and `updated_at` timestamps and updates on balance change.

### 8. Exceptions (Design & Best Practices)
- Custom exceptions: `BankError`, `CurrencyMismatchError`, `InsufficientFundsError`, `AccountNotFoundError`, `InvalidOperationError`.
- Use **specific exceptions**; avoid bare `except:`.
- Use `raise` with meaningful messages; consider chaining (`raise X from e`) where helpful.
- Use `try/except/else/finally` in the Bank or I/O boundaries as appropriate (mock I/O in tests).

### 9. Magic/Dunder Methods
- Implement at least:
  - `Money`: `__add__`, `__sub__`, `__eq__`, ordering methods, `__repr__`.
  - `Account`: `__len__`, `__repr__`.
  - `Transaction`: `__hash__`, `__repr__`.

### 10. Best Practices
- Favor composition for helpers (e.g., `AuditLogger`).
- Keep classes cohesive; document public APIs with docstrings.
- Log or surface errors appropriately in tests (no print spam).

---

## Non‑Functional
- Python 3.10+.
- No third‑party deps for core; `pytest` allowed but we also provide `unittest`-based tests.
- Deterministic tests (no network, no sleeping).
- Clear README and docstrings.
