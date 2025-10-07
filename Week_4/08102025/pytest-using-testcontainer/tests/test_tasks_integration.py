# tests/test_tasks_integration.py
import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from app.main import app
from app.database import get_db

@pytest.fixture(autouse=True)
def override_db_dep(db_session):
    # IMPORTANT: FastAPI expects a generator FUNCTION, not a generator object.
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_create_and_list_tasks():
    # create
    resp = client.post("/tasks", json={"title": "Write tests"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Write tests"
    assert data["done"] is False

    # list
    resp = client.get("/tasks")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["title"] == "Write tests"
