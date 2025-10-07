# PROBLEM.md — Problem Understanding & Requirements

## Context
You’re teaching/learning integration testing using Python, FastAPI, SQLAlchemy, Pydantic, and logging. The goal is to run automated integration tests that spin up real services with Testcontainers on a Windows laptop using Docker Desktop.

## What we’ll build
A tiny Task Manager API that lets you create and list tasks:
- POST /tasks → create a task (title, done=false by default)
- GET /tasks → list all tasks

## Why Testcontainers (even if app uses SQLite)?
- SQLite is file‑based and great for local/dev, but it’s not a containerized service; Testcontainers shines when starting real external dependencies.
- We’ll develop with SQLite (simple and zero‑install) and test with PostgreSQL via Testcontainers to simulate a realistic production DB, while keeping the classroom setup simple.

## Success criteria
1. Run app locally with SQLite.
2. Run pytest which
   - starts a throwaway PostgreSQL container with Testcontainers,
   - applies schema automatically,
   - runs requests against the FastAPI app,
   - tears everything down cleanly.
3. Students can repeat all steps on Windows + Docker Desktop.

## Non-goals (to keep it focused)
- No ORMs beyond SQLAlchemy Core/ORM basics.
- No Alembic migrations (we’ll use create_all in tests/startup to stay beginner‑friendly).
- No auth/security.

---

# Project Structure
```
fastapi-testcontainers-demo/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ crud.py
│  ├─ main.py
│  └─ logging_conf.py
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py
│  └─ test_tasks_integration.py
├─ .env.example
├─ requirements.txt
├─ README.md
└─ PROBLEM.md
```

# Steps (summary)
See README.md for quick start and run `pytest -q` to execute integration tests (Docker Desktop must be running).
