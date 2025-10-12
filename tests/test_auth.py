import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db import Base
from app.main import app
from app.models import User
from tests.conftest import client
from app.utils.auth import PasswordManager

# --- Register Tests ---


def test_register_user(client: TestClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }

    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_register_existing_user(client: TestClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }

    client.post("/auth/signup", json=payload)

    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 409 or response.status_code == 400
    data = response.json()
    assert data["detail"] == "User already exists"

# --- Login Tests ---


def test_signin_user(client: TestClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    client.post("/auth/signup", json=payload)

    response = client.post("/auth/signin", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"


def test_signin_invalid_credentials(client: TestClient):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    client.post("/auth/signup", json=payload)

    payload_invalid = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123456"
    }
    response = client.post("/auth/signin", json=payload_invalid)

    assert response.status_code == 403 or response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid credentials"
