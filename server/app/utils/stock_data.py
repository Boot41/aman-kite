import requests
from sqlalchemy.orm import Session
from app.config import settings
from app.models.stock import Stock

def fetch_stock_data(ticker_symbol: str):
    """Fetch real-time stock data from Finnhub API"""
    try:
        if settings.FINNHUB_API_KEY == "demo":
            # Mock data for demo purposes
            return {
                "price": 150.25,
                "change": 2.50,
                "change_percent": 1.69
            }
        
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker_symbol}&token={settings.FINNHUB_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Check if we got valid data
        if isinstance(data, dict) and 'c' in data and data['c'] is not None:
            current_price = float(data['c'])  # Current price
            daily_change = float(data['d'])   # Daily change
            daily_change_percent = float(data['dp'])  # Daily change percent
            
            return {
                "price": current_price,
                "change": daily_change,
                "change_percent": daily_change_percent
            }
        else:
            print(f"Invalid data received for {ticker_symbol}: {data}")
            return None
            
    except Exception as e:
        print(f"Error fetching stock data for {ticker_symbol}: {e}")
        return None

def update_stock_prices(db: Session):
    """Update all stock prices in the database"""
    stocks = db.query(Stock).all()
    for stock in stocks:
        stock_data = fetch_stock_data(stock.ticker_symbol)
        if stock_data:
            stock.current_price = stock_data["price"]
    db.commit()

def search_stocks(db: Session, query: str):
    """Search stocks by ticker symbol or company name"""
    return db.query(Stock).filter(
        (Stock.ticker_symbol.ilike(f"%{query}%")) | 
        (Stock.company_name.ilike(f"%{query}%"))
    ).all()