def test_sql_injection_attempts_blocked(client):
    assert client.get("/api/v1/slots", params={"practitioner_id":"1 OR 1=1"}).status_code == 422
    assert client.get("/api/v1/slots", params={"practitioner_id":"1; DROP TABLE practitioners"}).status_code == 422

    assert client.get("/api/v1/slots", params={"sort_by":"name"}).status_code == 422
    assert client.get("/api/v1/slots", params={"order":"descending"}).status_code == 422

    assert client.get("/api/v1/slots", params={"date_from":"not-a-date"}).status_code == 422

    assert client.get("/api/v1/slots", params={"limit":-1}).status_code == 422
    assert client.get("/api/v1/slots", params={"offset":-1}).status_code == 422

def test_global_exception_handler_is_used(client, monkeypatch):
    from app.services.practitioner_service import PractitionerService

    def boom(*args, **kwargs):
        raise Exception("kaboom")

    monkeypatch.setattr(PractitionerService, "list", boom, raising=True)
    r = client.get("/api/v1/practitioners")
    assert r.status_code == 500
    assert r.json().get("detail") == "Internal Server Error"
