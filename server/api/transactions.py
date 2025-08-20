from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.transaction import Transaction
from app.models.stock import Stock
from app.models.holding import Holding
from app.models.fund import Fund
from app.schemas.transaction import TransactionResponse, TransactionCreate, TradeRequest
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/portfolio/transactions", response_model=List[TransactionResponse])
def get_user_transactions(
    days: int = 30,  # Default to last 30 days
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get transaction history for the current user"""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    transactions = (
        db.query(
            Transaction.transaction_id,
            Transaction.user_id,
            Transaction.stock_id,
            Transaction.transaction_type,
            Transaction.quantity,
            Transaction.price_per_share,
            Transaction.transaction_date,
            Stock.ticker_symbol,
            Stock.company_name
        )
        .join(Stock, Transaction.stock_id == Stock.stock_id)
        .filter(
            Transaction.user_id == current_user.user_id,
            Transaction.transaction_date >= since_date
        )
        .order_by(Transaction.transaction_date.desc())
        .all()
    )
    
    response = []
    for transaction in transactions:
        response.append(TransactionResponse(
            transaction_id=transaction.transaction_id,
            user_id=transaction.user_id,
            stock_id=transaction.stock_id,
            transaction_type=transaction.transaction_type,
            quantity=transaction.quantity,
            price_per_share=float(transaction.price_per_share),
            transaction_date=transaction.transaction_date,
            ticker_symbol=transaction.ticker_symbol,
            company_name=transaction.company_name
        ))
    
    return response

@router.post("/trade/buy", response_model=dict)
def buy_stock(
    trade_request: TradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute a buy order"""
    # Check if stock exists
    stock = db.query(Stock).filter(Stock.stock_id == trade_request.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Check user funds
    user_funds = db.query(Fund).filter(Fund.user_id == current_user.user_id).first()
    total_cost = trade_request.quantity * stock.current_price
    
    if not user_funds or user_funds.balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Update user funds
    user_funds.balance -= total_cost
    
    # Create transaction record
    db_transaction = Transaction(
        user_id=current_user.user_id,
        stock_id=trade_request.stock_id,
        transaction_type="BUY",
        quantity=trade_request.quantity,
        price_per_share=stock.current_price
    )
    db.add(db_transaction)
    
    # Update or create holding
    holding = db.query(Holding).filter(
        Holding.user_id == current_user.user_id,
        Holding.stock_id == trade_request.stock_id
    ).first()
    
    if holding:
        # Update existing holding
        total_quantity = holding.quantity + trade_request.quantity
        total_cost = (holding.quantity * holding.average_cost) + (trade_request.quantity * stock.current_price)
        holding.average_cost = total_cost / total_quantity
        holding.quantity = total_quantity
    else:
        # Create new holding
        holding = Holding(
            user_id=current_user.user_id,
            stock_id=trade_request.stock_id,
            quantity=trade_request.quantity,
            average_cost=stock.current_price
        )
        db.add(holding)
    
    db.commit()
    return {"message": "Buy order executed successfully"}

@router.post("/trade/sell", response_model=dict)
def sell_stock(
    trade_request: TradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute a sell order"""
    # Check if stock exists
    stock = db.query(Stock).filter(Stock.stock_id == trade_request.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Check if user has enough shares
    holding = db.query(Holding).filter(
        Holding.user_id == current_user.user_id,
        Holding.stock_id == trade_request.stock_id
    ).first()
    
    if not holding or holding.quantity < trade_request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient shares")
    
    # Update user funds
    user_funds = db.query(Fund).filter(Fund.user_id == current_user.user_id).first()
    total_proceeds = trade_request.quantity * stock.current_price
    
    if user_funds:
        user_funds.balance += total_proceeds
    else:
        user_funds = Fund(user_id=current_user.user_id, balance=total_proceeds)
        db.add(user_funds)
    
    # Create transaction record
    db_transaction = Transaction(
        user_id=current_user.user_id,
        stock_id=trade_request.stock_id,
        transaction_type="SELL",
        quantity=trade_request.quantity,
        price_per_share=stock.current_price
    )
    db.add(db_transaction)
    
    # Update holding
    holding.quantity -= trade_request.quantity
    if holding.quantity == 0:
        db.delete(holding)
    
    db.commit()
    return {"message": "Sell order executed successfully"}