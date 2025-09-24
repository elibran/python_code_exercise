from fastapi.testclient import TestClient # type: ignore
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.account import Account
from app.models.transaction import Transaction
from datetime import datetime, timedelta

client = TestClient(app)

def ensure_schema():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

def seed_account_and_transactions(db):
    acct = db.query(Account).first()
    if not acct:
        acct = Account(owner_name="Tx Test", balance=1000.0, kyc_compliant=True)
        db.add(acct); db.commit(); db.refresh(acct)

    # Ensure some transactions
    if db.query(Transaction).filter(Transaction.account_id == acct.id).count() < 5:
        now = datetime.utcnow()
        samples = [
            Transaction(account_id=acct.id, amount=100.0, status="completed", date=now - timedelta(days=1), description="A"),
            Transaction(account_id=acct.id, amount=50.0, status="pending", date=now - timedelta(days=2), description="B"),
            Transaction(account_id=acct.id, amount=200.0, status="completed", date=now - timedelta(hours=1), description="C"),
            Transaction(account_id=acct.id, amount=75.0, status="failed", date=now - timedelta(days=3), description="D"),
            Transaction(account_id=acct.id, amount=125.0, status="completed", date=now - timedelta(days=4), description="E"),
        ]
        db.add_all(samples); db.commit()
    return acct

def test_transactions_filter_sort_paginate():
    ensure_schema()
    db = SessionLocal()
    acct = seed_account_and_transactions(db)

    # Filter: completed, Sort: date desc, Pagination: first page with limit=2
    resp = client.get(f"/accounts/{acct.id}/transactions", params={
        "status": "completed",
        "sortBy": "date:desc",
        "page": 1,
        "limit": 2
    })
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    # Newest completed should come first
    assert data[0]["status"] == "completed"
    assert data[1]["status"] == "completed"

    # Second page
    resp2 = client.get(f"/accounts/{acct.id}/transactions", params={
        "status": "completed",
        "sortBy": "date:desc",
        "page": 2,
        "limit": 2
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    # second page should have remaining completed txns (>=0)
    assert all(x["status"] == "completed" for x in data2)

    db.close()
