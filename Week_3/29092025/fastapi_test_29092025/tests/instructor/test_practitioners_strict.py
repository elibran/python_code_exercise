def test_practitioner_validation_and_status_codes(client):
    r = client.post("/api/v1/practitioners", json={"name":"", "specialty":"Dentist"})
    assert r.status_code == 422

    r = client.post("/api/v1/practitioners", json={"name":"A"*101, "specialty":"Dentist"})
    assert r.status_code == 422

    ids = []
    for nm in ["Dr1","Dr2","Dr3"]:
        r = client.post("/api/v1/practitioners", json={"name":nm,"specialty":"Dentist"})
        assert r.status_code == 201
        ids.append(r.json()["id"])

    r = client.get("/api/v1/practitioners", params={"limit":2,"offset":1})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2

    r = client.patch(f"/api/v1/practitioners/{ids[0]}")
    assert r.status_code in (405, 422)

    r = client.delete(f"/api/v1/practitioners/{ids[0]}")
    assert r.status_code == 204 and (r.text == "" or r.text is None)
