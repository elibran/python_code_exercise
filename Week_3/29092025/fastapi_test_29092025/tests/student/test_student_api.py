from datetime import datetime, timedelta

def test_practitioner_flow(client):
    r = client.post("/api/v1/practitioners", json={"name":"Dr A","specialty":"Dentist"})
    assert r.status_code == 201, r.text
    pid = r.json()["id"]
    assert r.json()["name"] == "Dr A"

    r = client.get("/api/v1/practitioners", params={"limit": 10, "offset": 0})
    assert r.status_code == 200
    assert isinstance(r.json(), list) and len(r.json()) >= 1

    r = client.get(f"/api/v1/practitioners/{pid}")
    assert r.status_code == 200 and r.json()["id"] == pid

    r = client.put(f"/api/v1/practitioners/{pid}", json={"name":"Dr B","specialty":"Ortho"})
    assert r.status_code == 200 and r.json()["name"] == "Dr B"

    r = client.delete(f"/api/v1/practitioners/{pid}")
    assert r.status_code == 204
    assert r.text in ("", None)

def test_slots_filters_and_booking_basic(client):
    p = client.post("/api/v1/practitioners", json={"name":"Dr A","specialty":"Dentist"}).json()
    now = datetime.utcnow()
    s1 = {"practitioner_id": p["id"], "start_time": (now+timedelta(hours=1)).isoformat(), "end_time": (now+timedelta(hours=2)).isoformat(), "is_booked": False}
    s2 = {"practitioner_id": p["id"], "start_time": (now+timedelta(hours=3)).isoformat(), "end_time": (now+timedelta(hours=4)).isoformat(), "is_booked": True}
    c1 = client.post("/api/v1/slots", json=s1).json()
    c2 = client.post("/api/v1/slots", json=s2).json()

    r = client.get("/api/v1/slots", params={"available": "true"})
    assert r.status_code == 200
    assert all(not s["is_booked"] for s in r.json())

    r = client.post(f"/api/v1/slots/{c2['id']}/book")
    assert r.status_code in (200, 409)
