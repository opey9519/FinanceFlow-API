from tests.conftest import client
from fastapi import responses


def test_health_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense Tracker API running!"}
