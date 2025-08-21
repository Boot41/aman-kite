#!/usr/bin/env python3
"""
Simple script to refresh stock prices using the existing utility function
"""

from app.database import SessionLocal
from app.utils.stock_data import update_stock_prices

def main():
    """Refresh all stock prices using the existing utility"""
    print("=== Refreshing Stock Prices ===")
    
    db = SessionLocal()
    try:
        print("Updating stock prices...")
        update_stock_prices(db)
        print("Stock prices updated successfully!")
        
    except Exception as e:
        print(f"Error updating stock prices: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
