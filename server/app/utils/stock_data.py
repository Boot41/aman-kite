import requests
from sqlalchemy.orm import Session
from app.config import settings
from app.models.stock import Stock

def fetch_stock_data(ticker_symbol: str):
    """Fetch real-time stock data from Alpha Vantage API"""
    print(f"API Key: {settings.ALPHA_VANTAGE_API_KEY}")
    try:
        if settings.ALPHA_VANTAGE_API_KEY == "demo":
            # Mock data for demo purposes
            return {
                "price": 150.25,
                "change": 2.50,
                "change_percent": 1.69
            }
        
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_symbol}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            return {
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": float(quote.get("10. change percent", "0%").replace("%", ""))
            }
        return None
    except Exception as e:
        print(f"Error fetching stock data: {e}")
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