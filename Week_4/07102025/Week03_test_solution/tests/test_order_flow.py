from fastapi.testclient import TestClient # type: ignore
from pathlib import Path
from time import sleep

from main import app
from database import init_db, engine

def setup_function():
    # Ensure all connections are closed before touching the SQLite file (Windows file lock fix)
    try:
        engine.dispose()
    except Exception:
        pass

    db_file = Path("./app.db")
    if db_file.exists():
        # On Windows, a short retry loop helps if background tasks just finished writing
        for _ in range(5):
            try:
                db_file.unlink()
                break
            except PermissionError:
                sleep(0.05)

    notif = Path("./notifications.log")
    if notif.exists():
        for _ in range(5):
            try:
                notif.unlink()
                break
            except PermissionError:
                sleep(0.05)

    init_db()


def register_and_login(client: TestClient, email: str, password: str, role: str = "user") -> str:
    r = client.post("/auth/register", json={"email": email, "password": password, "role": role})
    assert r.status_code == 201, r.text
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_order_success_flow():
    # Use context manager so startup/shutdown fire and connections close per-test
    with TestClient(app) as client:
        token = register_and_login(client, "alice@example.com", "password123", "user")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"product_id": "P123", "quantity": 2, "price": 150.0}
        r = client.post("/orders", json=payload, headers=headers)
        assert r.status_code == 201, r.text
        data = r.json()
        assert data["status"] == "confirmed"

        # background notification should be written
        sleep(0.15)
        assert Path("./notifications.log").exists()


def test_order_payment_failure_rolls_back():
    with TestClient(app) as client:
        token = register_and_login(client, "bob@example.com", "password123", "user")
        headers = {"Authorization": f"Bearer {token}", "x-simulate-payment-failure": "1"}
        payload = {"product_id": "P999", "quantity": 1, "price": 10.0}
        r = client.post("/orders", json=payload, headers=headers)
        assert r.status_code == 400
        assert r.json()["error"].startswith("Payment")

        # ensure no orders persisted
        r = client.get("/orders", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json() == []


def test_role_based_visibility():
    with TestClient(app) as client:
        token_user = register_and_login(client, "carol@example.com", "pass", "user")
        token_admin = register_and_login(client, "admin@example.com", "adminpass", "admin")

        # user creates an order
        r = client.post("/orders", json={"product_id": "P42", "quantity": 1, "price": 99.0},
                        headers={"Authorization": f"Bearer {token_user}"})
        assert r.status_code == 201

        # user can see only their orders
        r = client.get("/orders", headers={"Authorization": f"Bearer {token_user}"})
        assert r.status_code == 200
        assert len(r.json()) == 1

        # admin can see all orders
        r = client.get("/orders", headers={"Authorization": f"Bearer {token_admin}"})
        assert r.status_code == 200
        assert len(r.json()) >= 1
