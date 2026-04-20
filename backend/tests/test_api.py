from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Sports Prediction API Running"}


def test_predict_returns_200():
    response = client.get("/predict?home=Lakers&away=Celtics")
    assert response.status_code == 200


def test_predict_returns_winner():
    response = client.get("/predict?home=Lakers&away=Celtics")
    data = response.json()
    assert data["predicted_winner"] in ["Lakers", "Celtics"]


def test_predict_confidence_range():
    response = client.get("/predict?home=Lakers&away=Celtics")
    data = response.json()
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_missing_params():
    response = client.get("/predict")
    assert response.status_code == 422  # FastAPI validation error
