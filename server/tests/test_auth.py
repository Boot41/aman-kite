
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import get_password_hash


def test_register(client: TestClient, db_session: Session):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_register_existing_user(client: TestClient, db_session: Session):
    client.post(
        "/api/auth/register",
        json={"username": "testuser1", "email": "test1@example.com", "password": "password"},
    )
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser1", "email": "test1@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email or username already registered"}


def test_login(client: TestClient, db_session: Session):
    # Create a user to login with
    hashed_password = get_password_hash("password")
    user = User(username="testlogin", email="testlogin@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        data={"username": "testlogin@example.com", "password": "password"},
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, db_session: Session):
    # Create a user to login with
    hashed_password = get_password_hash("password")
    user = User(username="testlogin2", email="testlogin2@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        data={"username": "testlogin2@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_get_current_user_info(client: TestClient, db_session: Session):
    # Create a user and login to get a token
    hashed_password = get_password_hash("password")
    user = User(username="testme", email="testme@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/auth/login",
        data={"username": "testme@example.com", "password": "password"},
    )
    token = login_response.json()["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["username"] == "testme"
    assert json_response["email"] == "testme@example.com"
