from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.holding import Holding
from app.models.stock import Stock
from app.schemas.holding import HoldingResponse
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[HoldingResponse])
def get_user_holdings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all holdings for the current user"""
    holdings = (
        db.query(
            Holding.holding_id,
            Holding.user_id,
            Holding.stock_id,
            Holding.quantity,
            Holding.average_cost,
            Stock.ticker_symbol,
            Stock.current_price
        )
        .join(Stock, Holding.stock_id == Stock.stock_id)
        .filter(Holding.user_id == current_user.user_id)
        .all()
    )
    
    response = []
    for holding in holdings:
        total_value = holding.quantity * holding.current_price
        total_cost = holding.quantity * holding.average_cost
        profit_loss = total_value - total_cost
        
        response.append(HoldingResponse(
            holding_id=holding.holding_id,
            user_id=holding.user_id,
            stock_id=holding.stock_id,
            quantity=holding.quantity,
            average_cost=float(holding.average_cost),
            ticker_symbol=holding.ticker_symbol,
            current_price=float(holding.current_price),
            total_value=float(total_value),
            profit_loss=float(profit_loss)
        ))
    
    return response

@router.get("/{stock_id}", response_model=HoldingResponse)
def get_holding_by_stock(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific holding for a stock"""
    holding = (
        db.query(
            Holding.holding_id,
            Holding.user_id,
            Holding.stock_id,
            Holding.quantity,
            Holding.average_cost,
            Stock.ticker_symbol,
            Stock.current_price
        )
        .join(Stock, Holding.stock_id == Stock.stock_id)
        .filter(
            Holding.user_id == current_user.user_id,
            Holding.stock_id == stock_id
        )
        .first()
    )
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    total_value = holding.quantity * holding.current_price
    total_cost = holding.quantity * holding.average_cost
    profit_loss = total_value - total_cost
    
    return HoldingResponse(
        holding_id=holding.holding_id,
        user_id=holding.user_id,
        stock_id=holding.stock_id,
        quantity=holding.quantity,
        average_cost=float(holding.average_cost),
        ticker_symbol=holding.ticker_symbol,
        current_price=float(holding.current_price),
        total_value=float(total_value),
        profit_loss=float(profit_loss)
    )