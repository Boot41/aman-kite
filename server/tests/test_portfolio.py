
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.models.user import User
from app.models.holding import Holding
from app.models.stock import Stock
from app.utils.auth import get_password_hash

@pytest.fixture(scope="function")
def test_user(db_session: Session):
    hashed_password = get_password_hash("password")
    user = User(username="testportfolio", email="testportfolio@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User):
    login_response = client.post(
        "/api/auth/login",
        data={"username": "testportfolio@example.com", "password": "password"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_portfolio_current_value_no_holdings(client: TestClient, auth_headers: dict):
    response = client.get("/api/portfolio/current-value", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["invested_value"] == 0.0
    assert data["current_value"] == 0.0
    assert data["profit_loss"] == 0.0
    assert data["profit_loss_percentage"] == 0.0
    assert data["holdings"] == []

def test_get_portfolio_current_value_with_holdings(client: TestClient, db_session: Session, auth_headers: dict, test_user: User):
    stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.0)
    stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.0)
    db_session.add_all([stock1, stock2])
    db_session.commit()

    holding1 = Holding(user_id=test_user.user_id, stock_id=stock1.stock_id, quantity=10, average_cost=140.0)
    holding2 = Holding(user_id=test_user.user_id, stock_id=stock2.stock_id, quantity=5, average_cost=2700.0)
    db_session.add_all([holding1, holding2])
    db_session.commit()

    response = client.get("/api/portfolio/current-value", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert data["invested_value"] == (10 * 140.0) + (5 * 2700.0)
    assert data["current_value"] == (10 * 150.0) + (5 * 2800.0)
    assert data["profit_loss"] == ((10 * 150.0) + (5 * 2800.0)) - ((10 * 140.0) + (5 * 2700.0))
    assert len(data["holdings"]) == 2

@patch("api.portfolio.fetch_stock_data")
def test_refresh_portfolio_prices(mock_fetch_stock_data, client: TestClient, db_session: Session, auth_headers: dict, test_user: User):
    stock1 = Stock(ticker_symbol="MSFT", company_name="Microsoft", current_price=300.0)
    db_session.add(stock1)
    db_session.commit()

    holding1 = Holding(user_id=test_user.user_id, stock_id=stock1.stock_id, quantity=10, average_cost=290.0)
    db_session.add(holding1)
    db_session.commit()

    mock_fetch_stock_data.return_value = {"price": 310.0}

    response = client.post("/api/portfolio/refresh-prices", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Updated 1 stock prices"
    assert data["updated_count"] == 1

    db_session.refresh(stock1)
    assert stock1.current_price == 310.0
    mock_fetch_stock_data.assert_called_once_with("MSFT")
