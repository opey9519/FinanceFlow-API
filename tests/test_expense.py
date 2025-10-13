import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db import Base
from app.main import app
from app.models import User
from tests.conftest import client
from app.utils.auth import PasswordManager
from tests.test_auth import test_register_user, test_signin_user

# --- Create/Signin Fixture---


@pytest.fixture
def test_user(client: TestClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    client.post("/auth/signup", json=payload)
    response = client.post("/auth/signin", json=payload)

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return {"headers": headers, "payload": payload}

# --- Create Expenses ---


def test_create_expense(client: TestClient, test_user):
    expense_data = {
        "description": "Weekly grocery shopping",
        "amount": 45.75,
    }

    response = client.post("/expense/", json=expense_data,
                           headers=test_user["headers"])
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == expense_data["description"]
    assert data["amount"] == expense_data["amount"]
    assert "id" in data

# --- Get Expense(s) ---


def test_get_all_expenses(client: TestClient, test_user):
    response = client.get("/expense/", headers=test_user["headers"])
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_expense(client: TestClient, test_user):
    expense_data = {
        "description": "Weekly grocery shopping",
        "amount": 45.75,
    }
    create_resp = client.post(
        "/expense/", json=expense_data, headers=test_user["headers"])
    create_id = create_resp.json()["id"]

    response = client.get(
        f"/expense/{create_id}", headers=test_user["headers"])
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == create_id
    assert data["description"] == expense_data["description"]

# --- Update Expense ---


def test_update_expense(client: TestClient, test_user):
    # Create expense
    expense_data = {
        "description": "Weekly grocery shopping",
        "amount": 45.75,
    }
    create_resp = client.post(
        "/expense/", json=expense_data, headers=test_user["headers"])
    create_id = create_resp.json()["id"]

    # Update expense
    update_expense_data = {
        "description": "Monthly grocery shopping",
        "amount": 45.75 * 4,
    }

    update_resp = client.put(
        f"/expense/{create_id}", json=update_expense_data, headers=test_user["headers"])
    update_data = update_resp.json()

    assert update_resp.status_code == 200
    assert update_data["amount"] == update_expense_data["amount"]
    assert update_data["description"] == update_expense_data["description"]


# --- Delete Expense ---
def test_delete_expense(client: TestClient, test_user):
    # Create Expense
    expense_data = {
        "description": "Weekly grocery shopping",
        "amount": 45.75,
    }
    create_resp = client.post(
        "/expense", json=expense_data, headers=test_user["headers"])
    expense_id = create_resp.json()["id"]

    # Delete Expense
    delete_resp = client.delete(
        f"/expense/{expense_id}", headers=test_user["headers"])
    delete_data = delete_resp.json()

    assert delete_resp.status_code == 200
    assert delete_data["id"] == expense_id
