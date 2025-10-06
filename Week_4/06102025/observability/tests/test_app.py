import json
import re
import logging
from fastapi.testclient import TestClient # type: ignore
from app.main import app, registry, LOGIN_ATTEMPTS
from app.logging_utils import configure_json_logging, set_correlation_id, log_event

client = TestClient(app)

def parse_counter(metrics_text: str, metric: str, labels: dict[str, str]) -> float:
    # Build a regex like: login_attempts_total{status="success"} 3.0
    label_str = ",".join([f'{k}="{v}"' for k,v in labels.items()])
    pattern = rf"^{metric}\{{{label_str}\}}\s+([0-9\.]+)$"
    for line in metrics_text.splitlines():
        m = re.match(pattern, line)
        if m:
            return float(m.group(1))
    return 0.0

def test_metrics_endpoint_content_type():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/plain")

def test_health_endpoint_up_or_down():
    resp = client.get("/health")
    assert resp.status_code in (200, 503)
    data = resp.json()
    if resp.status_code == 200:
        assert data.get("status") == "UP"
    else:
        assert data.get("status") == "DOWN"

def test_login_metrics_success_and_failure_increment():
    # baseline
    before = client.get("/metrics").text
    s0 = parse_counter(before, "login_attempts_total", {"status":"success"})
    f0 = parse_counter(before, "login_attempts_total", {"status":"failure"})

    # one success
    good = client.post("/login", json={"username":"admin","password":"password"})
    assert good.status_code == 200

    # one failure
    bad = client.post("/login", json={"username":"admin","password":"nope"})
    assert bad.status_code == 401

    after = client.get("/metrics").text
    s1 = parse_counter(after, "login_attempts_total", {"status":"success"})
    f1 = parse_counter(after, "login_attempts_total", {"status":"failure"})
    assert s1 == s0 + 1.0
    assert f1 == f0 + 1.0

def test_transfer_success_and_failure_paths():
    # success
    ok = client.post("/transfer", json={
        "userId":"u1","fromAccount":"A","toAccount":"B","amount":5000
    })
    assert ok.status_code == 200
    assert ok.json().get("status") == "COMPLETED"

    # failure: exceeds limit
    bad = client.post("/transfer", json={
        "userId":"u1","fromAccount":"A","toAccount":"B","amount":10001
    })
    assert bad.status_code == 400
    body = bad.json()
    assert body.get("status") == "FAILED"
    assert "Exceeds transfer limit" in body.get("reason","")

def test_correlation_id_propagates():
    cid = "pytest-123"
    r = client.get("/health", headers={"X-Correlation-Id": cid})
    assert r.headers.get("X-Correlation-Id") == cid

def test_json_logging_with_correlation_and_context(capsys):
    # Reconfigure logging to ensure our formatter is active
    configure_json_logging()

    # Set a known correlation id, emit a log with context
    cid = set_correlation_id("pytest-cid")
    log_event(logging.INFO, "Testing structured log", userId="u1", feature="unit-test")

    captured = capsys.readouterr()
    # Find a JSON line in captured output
    line = next((ln for ln in captured.err.splitlines() + captured.out.splitlines() if ln.strip().startswith("{")), None)
    assert line is not None, "No JSON log line captured"

    payload = json.loads(line)
    assert payload.get("message") == "Testing structured log"
    assert payload.get("correlationId") == cid
    ctx = payload.get("context") or {}
    assert ctx.get("userId") == "u1"
    assert ctx.get("feature") == "unit-test"
