from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.stock import Stock
from app.schemas.stock import StockResponse, StockSearchResponse, StockDetailResponse
from app.utils.stock_data import fetch_stock_data, search_stocks, update_stock_prices
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[StockResponse])
def get_all_stocks(db: Session = Depends(get_db)):
    """Get all available stocks"""
    return db.query(Stock).all()

@router.get("/market-overview")
def get_market_overview(db: Session = Depends(get_db)):
    """Get stocks with real-time data for market overview"""
    # Get popular stocks that are more likely to have real-time data
    popular_tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']
    market_data = []
    
    for ticker in popular_tickers:
        stock = db.query(Stock).filter(Stock.ticker_symbol == ticker).first()
        if not stock:
            continue
            
        stock_data = fetch_stock_data(stock.ticker_symbol)
        if stock_data:
            stock.current_price = stock_data["price"]
            change = stock_data["change"]
            change_percent = stock_data["change_percent"]
        else:
            change = 0.0
            change_percent = 0.0
            
        market_data.append({
            "stock_id": stock.stock_id,
            "ticker_symbol": stock.ticker_symbol,
            "company_name": stock.company_name,
            "current_price": float(stock.current_price),
            "change": change,
            "change_percent": change_percent,
            "last_updated": stock.last_updated
        })
    
    db.commit()
    return market_data

@router.get("/search", response_model=List[StockSearchResponse])
def search_stocks_route(q: str, db: Session = Depends(get_db)):
    """Search stocks by ticker symbol or company name"""
    stocks = search_stocks(db, q)
    return stocks

@router.get("/{ticker_symbol}", response_model=StockDetailResponse)
def get_stock_details(ticker_symbol: str, db: Session = Depends(get_db)):
    """Get detailed information for a specific stock"""
    stock = db.query(Stock).filter(Stock.ticker_symbol == ticker_symbol.upper()).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Fetch real-time data
    stock_data = fetch_stock_data(ticker_symbol)
    
    if stock_data:
        stock.current_price = stock_data["price"]
        db.commit()
        db.refresh(stock)

    response_data = {
        "stock_id": stock.stock_id,
        "ticker_symbol": stock.ticker_symbol,
        "company_name": stock.company_name,
        "current_price": stock.current_price,
        "last_updated": stock.last_updated
    }
    
    if stock_data:
        response_data["historical_data"] = stock_data
    
    return response_data

@router.post("/refresh")
def refresh_all_stocks(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Refresh current_price for all stocks in the database."""
    try:
        update_stock_prices(db)
        return {"message": "Stock prices refreshed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh stock prices: {str(e)}")