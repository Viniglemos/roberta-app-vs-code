from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_score_endpoint_success():
    payload = {"metrics": {"accuracy": 0.9, "latency": 0.6}}

    response = client.post("/score", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 0.75
    assert data["status"] == "pass"


def test_score_endpoint_validation_error():
    response = client.post("/score", json={"metrics": {"accuracy": 2}})

    assert response.status_code == 400
    assert "between 0 and 1" in response.json()["detail"][0]
