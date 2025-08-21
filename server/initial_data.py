#!/usr/bin/env python3
"""
Script to populate the database with initial stock data with real-time prices
"""

import asyncio
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.stock import Stock
from app.database import Base
from app.utils.stock_data import fetch_stock_data

def create_initial_stocks():
    """Create initial stock data with real-time prices"""
    db = SessionLocal()
    try:
        # Check if stocks already exist
        existing_stocks = db.query(Stock).count()
        if existing_stocks > 0:
            print("Stocks already exist in database")
            return
        
        # Sample stock data with company names (prices will be fetched)
        stock_info = [
            {"ticker_symbol": "AAPL", "company_name": "Apple Inc."},
            {"ticker_symbol": "GOOGL", "company_name": "Alphabet Inc."},
            {"ticker_symbol": "MSFT", "company_name": "Microsoft Corporation"},
            {"ticker_symbol": "AMZN", "company_name": "Amazon.com Inc."},
            {"ticker_symbol": "TSLA", "company_name": "Tesla Inc."},
            {"ticker_symbol": "NVDA", "company_name": "NVIDIA Corporation"},
            {"ticker_symbol": "JPM", "company_name": "JPMorgan Chase & Co."},
            {"ticker_symbol": "V", "company_name": "Visa Inc."},
            {"ticker_symbol": "WMT", "company_name": "Walmart Inc."},
            {"ticker_symbol": "DIS", "company_name": "The Walt Disney Company"},
            {"ticker_symbol": "NFLX", "company_name": "Netflix Inc."},
            {"ticker_symbol": "ADBE", "company_name": "Adobe Inc."},
            {"ticker_symbol": "PYPL", "company_name": "PayPal Holdings Inc."},
            {"ticker_symbol": "INTC", "company_name": "Intel Corporation"},
            {"ticker_symbol": "CSCO", "company_name": "Cisco Systems Inc."},
            {"ticker_symbol": "PEP", "company_name": "PepsiCo Inc."},
            {"ticker_symbol": "KO", "company_name": "The Coca-Cola Company"},
            {"ticker_symbol": "XOM", "company_name": "Exxon Mobil Corporation"},
            {"ticker_symbol": "CVX", "company_name": "Chevron Corporation"},
            {"ticker_symbol": "IBM", "company_name": "International Business Machines Corporation"},
        ]
        
        print("Fetching real-time stock prices...")
        initial_stocks = []
        
        for i, info in enumerate(stock_info):
            ticker = info["ticker_symbol"]
            company_name = info["company_name"]
            
            print(f"Fetching price for {ticker} ({i+1}/{len(stock_info)})...")
            
            # Fetch real-time price
            stock_data_result = fetch_stock_data(ticker)
            current_price = stock_data_result["price"] if stock_data_result else None
            
            if current_price is None:
                print(f"Warning: Could not fetch price for {ticker}, skipping...")
                continue
            
            stock_data = {
                "ticker_symbol": ticker,
                "company_name": company_name,
                "current_price": current_price
            }
            initial_stocks.append(stock_data)
            
            # Add delay to avoid API rate limits (Alpha Vantage allows 5 calls per minute)
            if i < len(stock_info) - 1:  # Don't sleep after the last stock
                print("Waiting 12 seconds to avoid API rate limits...")
                time.sleep(12)
        
        # Add stocks to database
        for stock_data in initial_stocks:
            stock = Stock(**stock_data)
            db.add(stock)
        
        db.commit()
        print(f"Successfully added {len(initial_stocks)} stocks with real-time prices to the database")
        
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