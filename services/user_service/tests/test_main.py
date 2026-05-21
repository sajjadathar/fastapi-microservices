from fastapi.testclient import TestClient

from main import app

# from db import get_session
from services.user_service.db import get_session

from unittest.mock import MagicMock
import pytest



# client = TestClient(app)

@pytest.fixture
def client():
    return TestClient(app)

def override_get_session_success():
    mock_session = MagicMock()
    mock_session.exec.return_value = "ok"
    yield mock_session

@pytest.fixture
def client():
    return TestClient(app)

def test_liveness_probe(client):
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_probe_success(client):
    app.dependency_overrides[get_session] = override_get_session_success

    response = client.get("/health/readiness")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

    app.dependency_overrides.clear()

def override_get_session_failure():
    mock_session = MagicMock()
    mock_session.exec.side_effect = Exception("DB connection failed")
    yield mock_session


def test_readiness_probe_failure(client):
    app.dependency_overrides[get_session] = override_get_session_failure

    response = client.get("/health/readiness")

    assert response.status_code == 503
    assert response.json()["status"] == "unhealthy"
    assert "DB connection failed" in response.json()["detail"]

    app.dependency_overrides.clear()