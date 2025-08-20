
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.fund import Fund
from app.utils.auth import get_password_hash


@pytest.fixture
def authenticated_client(client: TestClient, db_session: Session):
    # Create a user and login to get a token
    hashed_password = get_password_hash("password")
    user = User(username="testfunds", email="testfunds@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/auth/login",
        data={"username": "testfunds@example.com", "password": "password"},
    )
    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


def test_get_user_funds(authenticated_client: TestClient, db_session: Session):
    response = authenticated_client.get("/api/portfolio/funds/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["balance"] == 0.00


def test_add_funds(authenticated_client: TestClient, db_session: Session):
    response = authenticated_client.post("/api/portfolio/funds/add", json={"amount": 100.50})
    assert response.status_code == 200
    assert response.json() == {"message": "Funds added successfully"}

    # Check if the balance was updated
    user = db_session.query(User).filter(User.email == "testfunds@example.com").first()
    fund = db_session.query(Fund).filter(Fund.user_id == user.user_id).first()
    assert fund.balance == 100.50


def test_withdraw_funds(authenticated_client: TestClient, db_session: Session):
    # Add funds first
    authenticated_client.post("/api/portfolio/funds/add", json={"amount": 200.00})

    response = authenticated_client.post("/api/portfolio/funds/withdraw", json={"amount": 50.00})
    assert response.status_code == 200
    assert response.json() == {"message": "Withdrawal successful"}

    # Check if the balance was updated
    user = db_session.query(User).filter(User.email == "testfunds@example.com").first()
    fund = db_session.query(Fund).filter(Fund.user_id == user.user_id).first()
    assert fund.balance == 150.00


def test_withdraw_insufficient_funds(authenticated_client: TestClient):
    response = authenticated_client.post("/api/portfolio/funds/withdraw", json={"amount": 1000.00})
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}
