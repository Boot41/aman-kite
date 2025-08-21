#!/usr/bin/env python3
"""Debug portfolio analysis issue"""

from app.database import SessionLocal
from app.models.user import User
from app.models.holding import Holding
from app.models.stock import Stock
from app.models.fund import Fund
from app.utils.ai_service import AIService
from app.utils.auth import get_password_hash

def create_test_user_with_holdings():
    """Create a test user with some holdings"""
    db = SessionLocal()
    try:
        # Check if test user exists
        test_user = db.query(User).filter(User.username == "portfoliotest").first()
        if not test_user:
            # Create test user
            test_user = User(
                username="portfoliotest",
                email="portfolio@test.com",
                password_hash=get_password_hash("testpass"),
                first_name="Portfolio",
                last_name="Test"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"Created test user: {test_user.username} (ID: {test_user.user_id})")
        
        # Add funds
        fund = db.query(Fund).filter(Fund.user_id == test_user.user_id).first()
        if not fund:
            fund = Fund(user_id=test_user.user_id, balance=10000.0)
            db.add(fund)
            db.commit()
            print(f"Added $10,000 in funds")
        
        # Check if holdings exist
        existing_holdings = db.query(Holding).filter(Holding.user_id == test_user.user_id).count()
        if existing_holdings == 0:
            # Get some stocks
            stocks = db.query(Stock).limit(3).all()
            if stocks:
                for i, stock in enumerate(stocks):
                    holding = Holding(
                        user_id=test_user.user_id,
                        stock_id=stock.stock_id,
                        quantity=10 + i * 5,
                        average_cost=float(stock.current_price) * 0.95  # Simulate some profit
                    )
                    db.add(holding)
                
                db.commit()
                print(f"Created {len(stocks)} test holdings")
        
        # Test AI portfolio analysis
        ai_service = AIService()
        print("\n=== Testing Portfolio Analysis ===")
        
        try:
            overview = ai_service.get_portfolio_overview(test_user.user_id, db)
            print(f"Portfolio Analysis Result: {overview[:200]}...")
            return True
        except Exception as e:
            print(f"Portfolio Analysis Error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user_with_holdings()
