#!/usr/bin/env python3
"""
Script to refresh existing stock data with real-time prices from Alpha Vantage
"""

import time
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.stock import Stock
from app.database import Base
from app.utils.stock_data import fetch_stock_data

def refresh_stock_prices():
    """Refresh all existing stock prices with real-time data"""
    db = SessionLocal()
    try:
        # Get all existing stocks
        stocks = db.query(Stock).all()
        
        if not stocks:
            print("No stocks found in database. Run initial_data.py first.")
            return
        
        print(f"Found {len(stocks)} stocks to refresh...")
        updated_count = 0
        
        for i, stock in enumerate(stocks):
            ticker = stock.ticker_symbol
            old_price = stock.current_price
            
            print(f"Refreshing {ticker} ({i+1}/{len(stocks)}) - Current: ${old_price}")
            
            # Fetch real-time price
            stock_data_result = fetch_stock_data(ticker)
            new_price = stock_data_result["price"] if stock_data_result else None
            
            if new_price is None:
                print(f"Warning: Could not fetch price for {ticker}, keeping old price")
                continue
            
            # Update the stock price
            stock.current_price = new_price
            updated_count += 1
            
            print(f"Updated {ticker}: ${old_price} -> ${new_price}")
            
            # Add delay to avoid API rate limits (Alpha Vantage allows 5 calls per minute)
            if i < len(stocks) - 1:  # Don't sleep after the last stock
                print("Waiting 12 seconds to avoid API rate limits...")
                time.sleep(12)
        
        db.commit()
        print(f"\nSuccessfully updated {updated_count} out of {len(stocks)} stock prices")
        
    except Exception as e:
        print(f"Error refreshing stock prices: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Stock Price Refresh Script ===")
    refresh_stock_prices()
    print("Stock price refresh completed!")
