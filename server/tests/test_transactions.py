import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.user import User
from app.models.stock import Stock
from app.models.transaction import Transaction
from app.models.holding import Holding
from app.models.fund import Fund
from app.utils.auth import get_password_hash


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    hashed_password = get_password_hash("password")
    user = User(username="testtransactions", email="testtransactions@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User):
    login_response = client.post(
        "/api/auth/login",
        data={"username": "testtransactions@example.com", "password": "password"},
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


@pytest.fixture(scope="function")
def sample_transactions(db_session: Session, test_user: User, sample_stocks):
    transactions = [
        Transaction(
            user_id=test_user.user_id,
            stock_id=sample_stocks[0].stock_id,
            transaction_type="buy",
            quantity=10,
            price_per_share=140.0,
            transaction_date=datetime.now() - timedelta(days=5)
        ),
        Transaction(
            user_id=test_user.user_id,
            stock_id=sample_stocks[1].stock_id,
            transaction_type="buy",
            quantity=5,
            price_per_share=2700.0,
            transaction_date=datetime.now() - timedelta(days=3)
        ),
        Transaction(
            user_id=test_user.user_id,
            stock_id=sample_stocks[0].stock_id,
            transaction_type="sell",
            quantity=3,
            price_per_share=155.0,
            transaction_date=datetime.now() - timedelta(days=1)
        )
    ]
    db_session.add_all(transactions)
    db_session.commit()
    return transactions


def test_get_transactions_unauthorized(client: TestClient):
    response = client.get("/api/portfolio/transactions")
    assert response.status_code == 401


def test_get_transactions_empty(client: TestClient, auth_headers: dict):
    response = client.get("/api/portfolio/transactions", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_transactions_with_data(client: TestClient, auth_headers: dict, sample_transactions):
    response = client.get("/api/portfolio/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Most recent first
    assert data[0]["transaction_type"].upper() == "SELL"
    assert data[0]["quantity"] == 3
    assert data[0]["price_per_share"] == 155.0
    assert data[0]["ticker_symbol"] == "AAPL"
    assert data[1]["transaction_type"].upper() == "BUY"
    assert data[1]["quantity"] == 5
    assert data[1]["ticker_symbol"] == "GOOGL"
    assert data[2]["transaction_type"].upper() == "BUY"
    assert data[2]["quantity"] == 10
    assert data[2]["ticker_symbol"] == "AAPL"


def test_get_transactions_days_filter(client: TestClient, auth_headers: dict, sample_transactions):
    # Only include last 2 days => should include just the sell tx
    response = client.get("/api/portfolio/transactions?days=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["transaction_type"].upper() == "SELL"


def test_get_transactions_company_fields(client: TestClient, auth_headers: dict, sample_transactions):
    # Ensure ticker_symbol and company_name included
    response = client.get("/api/portfolio/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert all("ticker_symbol" in t and "company_name" in t for t in data)


def test_get_transactions_default_days(client: TestClient, auth_headers: dict, sample_transactions):
    # Default days=30 should include all 3
    response = client.get("/api/portfolio/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_trade_buy_unauthorized(client: TestClient):
    response = client.post("/api/trade/buy", json={"stock_id": 1, "quantity": 5})
    assert response.status_code == 401


def test_trade_buy_insufficient_funds(client: TestClient, auth_headers: dict, sample_stocks):
    # No funds setup
    response = client.post("/api/trade/buy", json={"stock_id": sample_stocks[0].stock_id, "quantity": 10}, headers=auth_headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient funds"}


def test_trade_buy_success_creates_holding_and_transaction(client: TestClient, db_session: Session, auth_headers: dict, test_user: User, sample_stocks):
    # Add funds
    db_session.add(Fund(user_id=test_user.user_id, balance=5000.0))
    db_session.commit()
    # Buy 10 shares of AAPL at current price 150.0
    response = client.post("/api/trade/buy", json={"stock_id": sample_stocks[0].stock_id, "quantity": 10}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Buy order executed successfully"}
    # Verify holding and funds
    holding = db_session.query(Holding).filter(Holding.user_id == test_user.user_id, Holding.stock_id == sample_stocks[0].stock_id).first()
    assert holding is not None and holding.quantity == 10 and holding.average_cost == 150.0
    fund = db_session.query(Fund).filter(Fund.user_id == test_user.user_id).first()
    assert round(fund.balance, 2) == 3500.0
    # Verify transaction exists
    tx = db_session.query(Transaction).filter(Transaction.user_id == test_user.user_id, Transaction.stock_id == sample_stocks[0].stock_id, Transaction.transaction_type == "BUY").first()
    assert tx is not None and tx.quantity == 10


def test_trade_sell_unauthorized(client: TestClient):
    response = client.post("/api/trade/sell", json={"stock_id": 1, "quantity": 1})
    assert response.status_code == 401


def test_trade_sell_fail_no_holding(client: TestClient, auth_headers: dict, sample_stocks):
    response = client.post("/api/trade/sell", json={"stock_id": sample_stocks[0].stock_id, "quantity": 1}, headers=auth_headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Insufficient shares"}


def test_trade_buy_invalid_stock(client: TestClient, auth_headers: dict):
    response = client.post("/api/trade/buy", json={"stock_id": 9999, "quantity": 1}, headers=auth_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock not found"}


def test_trade_sell_success_flow(client: TestClient, db_session: Session, auth_headers: dict, test_user: User, sample_stocks):
    # Setup: funds and initial holding via buy
    db_session.add(Fund(user_id=test_user.user_id, balance=10000.0))
    db_session.commit()
    client.post("/api/trade/buy", json={"stock_id": sample_stocks[0].stock_id, "quantity": 10}, headers=auth_headers)
    # Now sell 4 shares
    response = client.post("/api/trade/sell", json={"stock_id": sample_stocks[0].stock_id, "quantity": 4}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Sell order executed successfully"}
    holding = db_session.query(Holding).filter(Holding.user_id == test_user.user_id, Holding.stock_id == sample_stocks[0].stock_id).first()
    assert holding.quantity == 6
    fund = db_session.query(Fund).filter(Fund.user_id == test_user.user_id).first()
    # Initial balance 10000 - (10*150) + (4*150) = 10000 - 1500 + 600 = 9100
    assert round(fund.balance, 2) == 9100.0
