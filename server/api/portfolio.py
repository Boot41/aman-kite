from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.holding import Holding
from app.models.stock import Stock
from app.utils.auth import get_current_user
from app.utils.stock_data import fetch_stock_data
from app.models.user import User

router = APIRouter()

@router.get("/current-value")
def get_portfolio_current_value(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get real-time portfolio value with P&L calculations"""
    try:
        holdings = db.query(Holding).filter(Holding.user_id == current_user.user_id).all()
        
        portfolio_data = {
            "invested_value": 0.0,
            "current_value": 0.0,
            "profit_loss": 0.0,
            "profit_loss_percentage": 0.0,
            "holdings": []
        }
        
        for holding in holdings:
            stock = db.query(Stock).filter(Stock.stock_id == holding.stock_id).first()
            if not stock:
                continue
                
            # Get real-time stock data
            stock_data = fetch_stock_data(stock.ticker_symbol)
            if stock_data:
                current_price = stock_data["price"]
                daily_change = stock_data["change"]
                daily_change_percent = stock_data["change_percent"]
                # Update database with latest price
                stock.current_price = current_price
            else:
                current_price = float(stock.current_price)
                daily_change = 0.0
                daily_change_percent = 0.0
            
            # Calculate values
            invested_value = float(holding.quantity) * float(holding.average_cost)
            current_value = float(holding.quantity) * current_price
            pnl = current_value - invested_value
            pnl_percent = (pnl / invested_value * 100) if invested_value > 0 else 0.0
            
            holding_data = {
                "stock_id": stock.stock_id,
                "ticker_symbol": stock.ticker_symbol,
                "company_name": stock.company_name,
                "quantity": holding.quantity,
                "average_cost": float(holding.average_cost),
                "current_price": current_price,
                "invested_value": invested_value,
                "current_value": current_value,
                "pnl": pnl,
                "pnl_percent": pnl_percent,
                "change": daily_change,
                "change_percent": daily_change_percent
            }
            
            portfolio_data["holdings"].append(holding_data)
            portfolio_data["invested_value"] += invested_value
            portfolio_data["current_value"] += current_value
        
        portfolio_data["profit_loss"] = portfolio_data["current_value"] - portfolio_data["invested_value"]
        portfolio_data["profit_loss_percentage"] = (
            (portfolio_data["profit_loss"] / portfolio_data["invested_value"] * 100) 
            if portfolio_data["invested_value"] > 0 else 0.0
        )
        
        # Commit database updates
        db.commit()
        
        return portfolio_data
    except Exception as e:
        print(f"Error in get_portfolio_current_value: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/refresh-prices")
def refresh_portfolio_prices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually refresh all stock prices in user's portfolio"""
    holdings = db.query(Holding).filter(Holding.user_id == current_user.user_id).all()
    
    updated_count = 0
    for holding in holdings:
        stock = db.query(Stock).filter(Stock.stock_id == holding.stock_id).first()
        if stock:
            stock_data = fetch_stock_data(stock.ticker_symbol)
            if stock_data:
                stock.current_price = stock_data["price"]
                updated_count += 1
    
    db.commit()
    return {"message": f"Updated {updated_count} stock prices", "updated_count": updated_count}
