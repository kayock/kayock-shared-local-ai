import sys
from pathlib import Path

import pytest

TROPHY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TROPHY_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(TROPHY_ROOT))


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app import app
    return TestClient(app)


def test_homepage_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "TROPHY ROOM" in resp.text
    assert "your-local-key" not in resp.text
    assert "Bearer sk-" not in resp.text


def test_api_status(client):
    resp = client.get("/api/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "lemonade" in data
    assert "gpu" in data
    assert "services" in data
    body = resp.text.lower()
    assert "sk-" not in body
    assert "bearer " not in body or "redacted" in body


def test_api_evidence(client):
    resp = client.get("/api/evidence")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) >= 3
    assert all("10.0.0." not in (i.get("content") or "") for i in items)


def test_api_governor(client):
    resp = client.get("/api/governor")
    assert resp.status_code == 200
    data = resp.json()
    assert data["throughput"]["improvement_pct"] == 4.22
    assert data["throughput"]["winner"]["max_tokens"] == 480


def test_evidence_loading():
    from adapters.evidence import load_evidence_vault, load_milestones
    vault = load_evidence_vault()
    assert any(v["id"] == "throughput" for v in vault)
    milestones = load_milestones()
    assert any(m["title"].startswith("Father Fox") for m in milestones)


def test_sanitization():
    from adapters.evidence import _sanitize_display
    dirty = "client at 10.0.0.104 api_key=secret123"
    clean = _sanitize_display(dirty)
    assert "10.0.0.104" not in clean
    assert "secret123" not in clean


def test_governor_panel():
    from adapters.governor_data import get_governor_panel
    panel = get_governor_panel()
    assert panel["throughput"]["best_score"] > panel["throughput"]["baseline_score"]


def test_services_offline_graceful(monkeypatch):
    from adapters.services import probe_all_services

    def fail_probe(*a, **k):
        return False, "mock offline"

    monkeypatch.setattr("adapters.services._probe", fail_probe)
    services = probe_all_services()
    assert len(services) >= 5
    assert all(s.status in ("offline", "planned") for s in services)
