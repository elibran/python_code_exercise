from datetime import datetime, timedelta

def seed_practitioner(client, name="Dr A", specialty="Dentist"):
    return client.post("/api/v1/practitioners", json={"name":name,"specialty":specialty}).json()

def make_slot(pr_id, start, end, booked=False):
    return {"practitioner_id": pr_id, "start_time": start.isoformat(), "end_time": end.isoformat(), "is_booked": booked}

def test_slot_validation_filters_pagination_sorting(client):
    p = seed_practitioner(client)
    now = datetime.utcnow().replace(microsecond=0)

    bad = make_slot(p["id"], now, now, False)
    assert client.post("/api/v1/slots", json=bad).status_code == 422

    created = []
    for i in range(5):
        s = make_slot(p["id"], now+timedelta(hours=i), now+timedelta(hours=i+1), booked=(i%2==0))
        r = client.post("/api/v1/slots", json=s)
        assert r.status_code == 201, r.text
        created.append(r.json())

    r = client.get("/api/v1/slots", params={"available": "true"})
    assert r.status_code == 200
    assert all(not s["is_booked"] for s in r.json())

    r = client.get("/api/v1/slots", params={"available": "false"})
    assert r.status_code == 200
    assert all(s["is_booked"] for s in r.json())

    date_from = created[1]["start_time"]
    date_to = created[3]["end_time"]
    r = client.get("/api/v1/slots", params={"date_from": date_from, "date_to": date_to})
    assert r.status_code == 200
    subset = r.json()
    assert len(subset) >= 3

    r = client.get("/api/v1/slots", params={"sort_by":"start_time","order":"asc","limit":3,"offset":0})
    asc_list = r.json()
    assert all(asc_list[i]["start_time"] <= asc_list[i+1]["start_time"] for i in range(len(asc_list)-1))

    r = client.get("/api/v1/slots", params={"sort_by":"start_time","order":"desc","limit":3,"offset":0})
    desc_list = r.json()
    assert all(desc_list[i]["start_time"] >= desc_list[i+1]["start_time"] for i in range(len(desc_list)-1))

    r1 = client.get("/api/v1/slots", params={"limit":2, "offset":0, "sort_by":"start_time", "order":"asc"}).json()
    r2 = client.get("/api/v1/slots", params={"limit":2, "offset":2, "sort_by":"start_time", "order":"asc"}).json()
    if r2:
        assert r1[-1]["start_time"] <= r2[0]["start_time"]

def test_booking_conflict_and_missing(client):
    p = seed_practitioner(client)
    now = datetime.utcnow().replace(microsecond=0)
    s = make_slot(p["id"], now, now+timedelta(hours=1), False)
    slot = client.post("/api/v1/slots", json=s).json()

    r = client.post(f"/api/v1/slots/{slot['id']}/book")
    assert r.status_code == 200 and r.json()["is_booked"] is True

    r = client.post(f"/api/v1/slots/{slot['id']}/book")
    assert r.status_code == 409

    r = client.post("/api/v1/slots/999999/book")
    assert r.status_code == 404
