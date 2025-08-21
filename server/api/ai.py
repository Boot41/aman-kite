from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.stock import Stock
from app.utils.auth import get_current_user
from app.utils.ai_service import ai_service

router = APIRouter()

@router.get("/stock-insights/{ticker}")
def get_stock_insights(
    ticker: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered stock performance insights"""
    try:
        stock = db.query(Stock).filter(Stock.ticker_symbol == ticker.upper()).first()
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        # Mock historical data for demo
        historical_data = [
            {"date": "2024-08-20", "price": float(stock.current_price), "volume": 1000000},
            {"date": "2024-08-19", "price": float(stock.current_price) * 0.98, "volume": 950000},
            {"date": "2024-08-18", "price": float(stock.current_price) * 1.02, "volume": 1100000},
        ]
        
        insights = ai_service.get_stock_performance_insights(stock, historical_data)
        
        return {
            "ticker": ticker.upper(),
            "company_name": stock.company_name,
            "current_price": float(stock.current_price),
            "insights": insights,
            "generated_at": "2024-08-21T13:30:00Z"
        }
        
    except HTTPException as e:
        # Re-raise known HTTP errors (e.g., 404 for stock not found)
        raise e
    except Exception as e:
        print(f"Error in get_stock_insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate stock insights")

@router.get("/market-sentiment")
def get_market_sentiment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered market sentiment analysis"""
    try:
        # Get top stocks for sentiment analysis
        stocks = db.query(Stock).limit(10).all()
        symbols = [stock.ticker_symbol for stock in stocks]
        
        sentiment_data = ai_service.get_market_sentiment(symbols)
        
        return {
            "sentiment": sentiment_data["overall_sentiment"],
            "sentiment_score": sentiment_data["sentiment_score"],
            "summary": sentiment_data["summary"],
            # Use a default to avoid KeyError if upstream doesn't include this
            "news_count": sentiment_data.get("news_count", 0),
            "analyzed_symbols": symbols,
            "generated_at": "2024-08-21T13:30:00Z"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in get_market_sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze market sentiment")

@router.get("/portfolio-overview")
def get_portfolio_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered portfolio analysis"""
    try:
        overview = ai_service.get_portfolio_overview(current_user.user_id, db)
        
        return {
            "user_id": current_user.user_id,
            "overview": overview,
            "generated_at": "2024-08-21T13:30:00Z"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in get_portfolio_overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate portfolio overview")
