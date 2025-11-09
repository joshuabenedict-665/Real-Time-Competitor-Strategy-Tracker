import json
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_sentiment_basic():
    payload = {"texts": ["Amazing battery", "Terrible delivery"], "do_summary": False}
    r = client.post("/sentiment", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert len(data["results"]) == 2
