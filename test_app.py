
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"

def test_add_and_list_expenses(client):
    response = client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 150}
    )
    assert response.status_code == 201

    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json["total"] == 150

def test_reject_invalid_amount(client):
    response = client.post(
        "/expenses",
        json={"title": "Lunch", "amount": -10}
    )
    assert response.status_code == 400
