def test_openapi_contract(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    data = r.json()
    paths = data["paths"]
    assert "/api/v1/practitioners" in paths
    assert "/api/v1/slots" in paths

    slot_get = paths["/api/v1/slots"]["get"]
    params = {p["name"]: p for p in slot_get["parameters"]}
    assert params["limit"]["schema"]["maximum"] == 100
    assert set(params["sort_by"]["schema"].get("pattern", "").split("|")) == {"start_time", "end_time"}
    assert set(params["order"]["schema"].get("pattern", "").split("|")) == {"asc", "desc"}

def test_versioning_paths(client):
    assert client.get("/api/v1/practitioners").status_code in (200, 204)
    assert client.get("/api/practitioners").status_code in (404, 405)
    assert client.get("/v1/practitioners").status_code in (404, 405)
