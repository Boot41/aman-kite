import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.stock import Stock
from app.models.holding import Holding
from app.models.fund import Fund
from app.utils.auth import get_password_hash


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    hashed_password = get_password_hash("password")
    user = User(username="testholdings", email="testholdings@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User):
    login_response = client.post(
        "/api/auth/login",
        data={"username": "testholdings@example.com", "password": "password"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def sample_stocks(db_session: Session):
    stocks = [
        Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.0),
        Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.0),
        Stock(ticker_symbol="MSFT", company_name="Microsoft Corp.", current_price=300.0)
    ]
    db_session.add_all(stocks)
    db_session.commit()
    return stocks


def test_get_holdings_unauthorized(client: TestClient):
    response = client.get("/api/portfolio/holdings/")
    assert response.status_code == 401


def test_get_holdings_empty(client: TestClient, auth_headers: dict):
    response = client.get("/api/portfolio/holdings/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_holdings_with_data(client: TestClient, db_session: Session, auth_headers: dict, test_user: User, sample_stocks):
    # Create holdings for the user
    holdings = [
        Holding(user_id=test_user.user_id, stock_id=sample_stocks[0].stock_id, quantity=10, average_cost=140.0),
        Holding(user_id=test_user.user_id, stock_id=sample_stocks[1].stock_id, quantity=5, average_cost=2700.0)
    ]
    db_session.add_all(holdings)
    db_session.commit()
    
    response = client.get("/api/portfolio/holdings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Check first holding
    holding1 = next(h for h in data if h["ticker_symbol"] == "AAPL")
    assert holding1["quantity"] == 10
    assert holding1["average_cost"] == 140.0
    assert holding1["current_price"] == 150.0
    
    # Check second holding
    holding2 = next(h for h in data if h["ticker_symbol"] == "GOOGL")
    assert holding2["quantity"] == 5
    assert holding2["average_cost"] == 2700.0


def test_get_holding_by_stock_unauthorized(client: TestClient):
    response = client.get("/api/portfolio/holdings/1")
    assert response.status_code == 401


def test_get_holding_by_stock_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/api/portfolio/holdings/999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Holding not found"}


def test_get_holding_by_stock_success(client: TestClient, db_session: Session, auth_headers: dict, test_user: User, sample_stocks):
    # Create holding for the user
    holding = Holding(user_id=test_user.user_id, stock_id=sample_stocks[0].stock_id, quantity=10, average_cost=140.0)
    db_session.add(holding)
    db_session.commit()
    
    response = client.get(f"/api/portfolio/holdings/{sample_stocks[0].stock_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 10
    assert data["average_cost"] == 140.0
    assert data["ticker_symbol"] == "AAPL"
    assert data["current_price"] == 150.0
    assert data["total_value"] == 1500.0  # 10 * 150
    assert data["profit_loss"] == 100.0   # 1500 - (10 * 140)
