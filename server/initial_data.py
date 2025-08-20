#!/usr/bin/env python3
"""
Script to populate the database with initial stock data
"""

import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.stock import Stock
from app.database import Base

def create_initial_stocks():
    """Create initial stock data"""
    db = SessionLocal()
    try:
        # Check if stocks already exist
        existing_stocks = db.query(Stock).count()
        if existing_stocks > 0:
            print("Stocks already exist in database")
            return
        
        # Sample stock data
        initial_stocks = [
            {"ticker_symbol": "AAPL", "company_name": "Apple Inc.", "current_price": 150.00},
            {"ticker_symbol": "GOOGL", "company_name": "Alphabet Inc.", "current_price": 2800.00},
            {"ticker_symbol": "MSFT", "company_name": "Microsoft Corporation", "current_price": 300.00},
            {"ticker_symbol": "AMZN", "company_name": "Amazon.com Inc.", "current_price": 3200.00},
            {"ticker_symbol": "TSLA", "company_name": "Tesla Inc.", "current_price": 700.00},
            {"ticker_symbol": "NVDA", "company_name": "NVIDIA Corporation", "current_price": 500.00},
            {"ticker_symbol": "JPM", "company_name": "JPMorgan Chase & Co.", "current_price": 150.00},
            {"ticker_symbol": "V", "company_name": "Visa Inc.", "current_price": 200.00},
            {"ticker_symbol": "WMT", "company_name": "Walmart Inc.", "current_price": 140.00},
            {"ticker_symbol": "DIS", "company_name": "The Walt Disney Company", "current_price": 90.00},
            {"ticker_symbol": "NFLX", "company_name": "Netflix Inc.", "current_price": 350.00},
            {"ticker_symbol": "ADBE", "company_name": "Adobe Inc.", "current_price": 450.00},
            {"ticker_symbol": "PYPL", "company_name": "PayPal Holdings Inc.", "current_price": 60.00},
            {"ticker_symbol": "INTC", "company_name": "Intel Corporation", "current_price": 40.00},
            {"ticker_symbol": "CSCO", "company_name": "Cisco Systems Inc.", "current_price": 50.00},
            {"ticker_symbol": "PEP", "company_name": "PepsiCo Inc.", "current_price": 160.00},
            {"ticker_symbol": "KO", "company_name": "The Coca-Cola Company", "current_price": 55.00},
            {"ticker_symbol": "XOM", "company_name": "Exxon Mobil Corporation", "current_price": 60.00},
            {"ticker_symbol": "CVX", "company_name": "Chevron Corporation", "current_price": 100.00},
            {"ticker_symbol": "IBM", "company_name": "International Business Machines Corporation", "current_price": 130.00},
        ]
        
        for stock_data in initial_stocks:
            stock = Stock(**stock_data)
            db.add(stock)
        
        db.commit()
        print(f"Added {len(initial_stocks)} stocks to the database")
        
    except Exception as e:
        print(f"Error creating initial stocks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial stocks
    create_initial_stocks()
    print("Initial data setup completed!")