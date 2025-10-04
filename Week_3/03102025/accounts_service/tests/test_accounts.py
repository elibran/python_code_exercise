# tests/test_accounts.py
import os
import tempfile
import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, Session # type: ignore
from sqlalchemy.pool import StaticPool # type: ignore

from app.main import app
from app.db.models import Base
from app.db.session import get_db

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a TestClient with an in-memory SQLite database.
    Ensures a clean DB is used for the duration of the module.
    """
    # In-memory SQLite shared across connections
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Create schema
    Base.metadata.create_all(bind=engine)

    # Override get_db dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Yield test client
    with TestClient(app) as client:
        yield client

    # ---- teardown ----
    app.dependency_overrides.clear()
    engine.dispose()  # dispose connections cleanly


def test_health_endpoint(test_client: TestClient):
    r = test_client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_reference_endpoint(test_client: TestClient):
    r = test_client.get("/reference/account-types")
    assert r.status_code == 200
    assert "SAVINGS" in r.json()


def test_crud_flow(test_client: TestClient):
    # Create
    payload = {"id": 1, "name": "Abinash", "type": "SAVINGS", "email": "abmishra@example.com"}
    r = test_client.post("/accounts", json=payload)
    assert r.status_code == 201, r.text
    assert r.json()["id"] == 1

    # Read
    r = test_client.get("/accounts/1")
    assert r.status_code == 200
    assert r.json()["email"] == "abmishra@example.com"

    # List with filter
    r = test_client.get("/accounts", params={"q": "abi"})
    assert r.status_code == 200
    assert any(a["id"] == 1 for a in r.json())

    # Update
    r = test_client.put("/accounts/1", json={"name": "Abinash Mishra"})
    assert r.status_code == 200
    assert r.json()["name"] == "Abinash Mishra"

    # Delete
    r = test_client.delete("/accounts/1")
    assert r.status_code == 204