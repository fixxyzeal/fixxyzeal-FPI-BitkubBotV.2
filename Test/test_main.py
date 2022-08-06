from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "FPI-Bitkub Bot v2"}


def test_read_trade():
    response = client.get("/bottrade")
    assert response.status_code == 200
    assert response.json() == {"msg": "bottrade working!"}
