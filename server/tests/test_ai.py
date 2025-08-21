import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

from app.models.user import User
from app.models.stock import Stock
from app.models.holding import Holding
from app.utils.auth import get_password_hash


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    hashed_password = get_password_hash("password")
    user = User(username="testai", email="testai@example.com", password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User):
    login_response = client.post(
        "/api/auth/login",
        data={"username": "testai@example.com", "password": "password"},
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


def test_get_stock_insights_unauthorized(client: TestClient):
    response = client.get("/api/ai/stock-insights/AAPL")
    assert response.status_code == 401


@patch("api.ai.ai_service.get_stock_performance_insights")
def test_get_stock_insights_success(mock_ai_service, client: TestClient, db_session: Session, auth_headers: dict, sample_stocks):
    mock_insights = {
        "summary": "Apple stock has shown strong performance with consistent growth.",
        "key_trends": ["Strong iPhone sales", "Services revenue growth", "Market expansion"],
        "risk_assessment": "low",
        "outlook": "positive"
    }
    mock_ai_service.return_value = mock_insights
    
    response = client.get("/api/ai/stock-insights/AAPL", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "company_name" in data
    assert "current_price" in data
    assert "insights" in data
    assert data["insights"] == mock_insights
    assert "generated_at" in data


def test_get_stock_insights_stock_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/api/ai/stock-insights/INVALID", headers=auth_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Stock not found"}


@patch("api.ai.ai_service.get_stock_performance_insights")
def test_get_stock_insights_ai_service_error(mock_ai_service, client: TestClient, db_session: Session, auth_headers: dict, sample_stocks):
    mock_ai_service.side_effect = Exception("AI service error")
    
    response = client.get("/api/ai/stock-insights/AAPL", headers=auth_headers)
    assert response.status_code == 500
    assert "Failed to generate stock insights" in response.json()["detail"]


def test_get_market_sentiment_unauthorized(client: TestClient):
    response = client.get("/api/ai/market-sentiment")
    assert response.status_code == 401


@patch("api.ai.ai_service.get_market_sentiment")
def test_get_market_sentiment_success(mock_ai_service, client: TestClient, auth_headers: dict):
    mock_sentiment = {
        "overall_sentiment": "positive",
        "sentiment_score": 0.7,
        "summary": "Market shows positive sentiment with strong tech sector performance.",
        "key_trends": ["Tech stocks rallying", "Market indices up", "Positive earnings reports"]
    }
    mock_ai_service.return_value = mock_sentiment
    
    response = client.get("/api/ai/market-sentiment", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # API maps overall_sentiment -> sentiment and returns additional fields
    assert data["sentiment"] == mock_sentiment["overall_sentiment"]
    assert data["sentiment_score"] == mock_sentiment["sentiment_score"]
    assert data["summary"] == mock_sentiment["summary"]
    assert "news_count" in data
    assert "analyzed_symbols" in data and isinstance(data["analyzed_symbols"], list)
    assert "generated_at" in data


@patch("api.ai.ai_service.get_market_sentiment")
def test_get_market_sentiment_ai_service_error(mock_ai_service, client: TestClient, auth_headers: dict):
    mock_ai_service.side_effect = Exception("Market sentiment service error")
    
    response = client.get("/api/ai/market-sentiment", headers=auth_headers)
    assert response.status_code == 500
    assert "Failed to analyze market sentiment" in response.json()["detail"]


def test_get_portfolio_overview_unauthorized(client: TestClient):
    response = client.get("/api/ai/portfolio-overview")
    assert response.status_code == 401


@patch("api.ai.ai_service.get_portfolio_overview")
def test_get_portfolio_overview_success(mock_ai_service, client: TestClient, db_session: Session, auth_headers: dict, test_user: User, sample_stocks):
    # Create some holdings for the user
    holdings = [
        Holding(user_id=test_user.user_id, stock_id=sample_stocks[0].stock_id, quantity=10, average_cost=140.0),
        Holding(user_id=test_user.user_id, stock_id=sample_stocks[1].stock_id, quantity=5, average_cost=2700.0)
    ]
    db_session.add_all(holdings)
    db_session.commit()
    
    mock_overview = {
        "performance_summary": "Your portfolio shows strong diversification with tech focus.",
        "diversification_analysis": "Well-balanced across large-cap tech stocks.",
        "top_performers": ["AAPL"],
        "underperformers": [],
        "risk_assessment": "medium",
        "recommendations": ["Consider adding some defensive stocks"]
    }
    mock_ai_service.return_value = mock_overview
    
    response = client.get("/api/ai/portfolio-overview", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # API returns wrapper with user_id and generated_at
    assert "user_id" in data
    assert "generated_at" in data
    assert data["overview"] == mock_overview


@patch("api.ai.ai_service.get_portfolio_overview")
def test_get_portfolio_overview_no_holdings(mock_ai_service, client: TestClient, auth_headers: dict):
    mock_overview = {
        "performance_summary": "No holdings found in your portfolio.",
        "diversification_analysis": "Portfolio is empty.",
        "top_performers": [],
        "underperformers": [],
        "risk_assessment": "none",
        "recommendations": ["Start by adding some diversified stocks"]
    }
    mock_ai_service.return_value = mock_overview
    
    response = client.get("/api/ai/portfolio-overview", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "No holdings found" in data["overview"]["performance_summary"]


@patch("api.ai.ai_service.get_portfolio_overview")
def test_get_portfolio_overview_ai_service_error(mock_ai_service, client: TestClient, auth_headers: dict):
    mock_ai_service.side_effect = Exception("Portfolio analysis error")
    
    response = client.get("/api/ai/portfolio-overview", headers=auth_headers)
    assert response.status_code == 500
    assert "Failed to generate portfolio overview" in response.json()["detail"]
