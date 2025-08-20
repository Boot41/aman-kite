
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.stock import Stock
from app.models.watchlist import Watchlist
from app.utils.auth import get_password_hash


@pytest.fixture
def authenticated_client_watchlist(client: TestClient, db_session: Session):
    # Create a user and login to get a token
    hashed_password = get_password_hash("password")
    user = User(username="testwatchlist", email="testwatchlist@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/auth/login",
        data={"username": "testwatchlist@example.com", "password": "password"},
    )
    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


def test_get_user_watchlist(authenticated_client_watchlist: TestClient, db_session: Session):
    response = authenticated_client_watchlist.get("/api/watchlist/")
    assert response.status_code == 200
    assert response.json() == []


def test_add_to_watchlist(authenticated_client_watchlist: TestClient, db_session: Session):
    # Add a stock to the database
    stock = Stock(ticker_symbol="TSLA", company_name="Tesla, Inc.", current_price=700.00)
    db_session.add(stock)
    db_session.commit()

    response = authenticated_client_watchlist.post("/api/watchlist/", json={"stock_id": stock.stock_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Stock added to watchlist"}

    # Check if the item was added
    user = db_session.query(User).filter(User.email == "testwatchlist@example.com").first()
    watchlist_item = db_session.query(Watchlist).filter(Watchlist.user_id == user.user_id).first()
    assert watchlist_item is not None


def test_add_to_watchlist_already_exists(authenticated_client_watchlist: TestClient, db_session: Session):
    # Add a stock and add it to the watchlist
    stock = Stock(ticker_symbol="NFLX", company_name="Netflix, Inc.", current_price=500.00)
    db_session.add(stock)
    db_session.commit()
    authenticated_client_watchlist.post("/api/watchlist/", json={"stock_id": stock.stock_id})

    # Try to add it again
    response = authenticated_client_watchlist.post("/api/watchlist/", json={"stock_id": stock.stock_id})
    assert response.status_code == 400
    assert response.json() == {"detail": "Stock already in watchlist"}


def test_remove_from_watchlist(authenticated_client_watchlist: TestClient, db_session: Session):
    # Add a stock and add it to the watchlist
    stock = Stock(ticker_symbol="DIS", company_name="The Walt Disney Company", current_price=180.00)
    db_session.add(stock)
    db_session.commit()
    authenticated_client_watchlist.post("/api/watchlist/", json={"stock_id": stock.stock_id})

    response = authenticated_client_watchlist.delete(f"/api/watchlist/{stock.stock_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Stock removed from watchlist"}

    # Check if the item was removed
    user = db_session.query(User).filter(User.email == "testwatchlist@example.com").first()
    watchlist_item = db_session.query(Watchlist).filter(Watchlist.user_id == user.user_id).first()
    assert watchlist_item is None
