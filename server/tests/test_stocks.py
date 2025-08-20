
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.stock import Stock


def test_get_all_stocks(client: TestClient, db_session: Session):
    # Add some stocks to the test database
    stock1 = Stock(ticker_symbol="AAPL", company_name="Apple Inc.", current_price=150.00)
    stock2 = Stock(ticker_symbol="GOOGL", company_name="Alphabet Inc.", current_price=2800.00)
    db_session.add_all([stock1, stock2])
    db_session.commit()

    response = client.get("/api/stocks/")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2
    assert json_response[0]["ticker_symbol"] == "AAPL"
    assert json_response[1]["ticker_symbol"] == "GOOGL"


def test_search_stocks(client: TestClient, db_session: Session):
    stock1 = Stock(ticker_symbol="MSFT", company_name="Microsoft Corporation", current_price=300.00)
    db_session.add(stock1)
    db_session.commit()

    response = client.get("/api/stocks/search?q=Micro")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 1
    assert json_response[0]["company_name"] == "Microsoft Corporation"


def test_get_stock_details(client: TestClient, db_session: Session):
    stock = Stock(ticker_symbol="AMZN", company_name="Amazon.com, Inc.", current_price=3400.00)
    db_session.add(stock)
    db_session.commit()

    response = client.get(f"/api/stocks/{stock.ticker_symbol}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["ticker_symbol"] == "AMZN"
    assert "historical_data" in json_response


def test_get_stock_details_not_found(client: TestClient, db_session: Session):
    response = client.get("/api/stocks/NONEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock not found"}
