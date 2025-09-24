from fastapi.testclient import TestClient # type: ignore
from app.main import app
from app.database import SessionLocal
from app.models.account import Account
from app.models.scheduled_payment import ScheduledPayment
import datetime

client = TestClient(app)

def test_create_and_delete_scheduled_payment():
    db = SessionLocal()
    # Ensure account exists
    account = db.query(Account).first()
    if not account:
        account = Account(name="Test Account", balance=1000)
        db.add(account)
        db.commit()
        db.refresh(account)

    # Create scheduled payment
    response = client.post(f"/accounts/{account.id}/scheduled-payments", json={
        "amount": 250.00,
        "scheduled_date": "2025-10-05T10:00:00",
        "description": "Test Payment"
    })
    assert response.status_code == 200
    data = response.json()
    payment_id = data["id"]

    # Delete scheduled payment
    delete_response = client.delete(f"/scheduled-payments/{payment_id}")
    assert delete_response.status_code == 200

    # Verify deleted
    deleted = db.query(ScheduledPayment).filter_by(id=payment_id).first()
    assert deleted is None

    db.close()
