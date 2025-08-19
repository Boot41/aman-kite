from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.fund import Fund
from app.schemas.fund import FundResponse, FundUpdate
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=FundResponse)
def get_user_funds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's fund balance"""
    funds = db.query(Fund).filter(Fund.user_id == current_user.user_id).first()
    
    if not funds:
        # Create fund record if it doesn't exist
        funds = Fund(user_id=current_user.user_id, balance=0.00)
        db.add(funds)
        db.commit()
        db.refresh(funds)
    
    return FundResponse(
        user_id=funds.user_id,
        balance=float(funds.balance)
    )

@router.post("/add", response_model=dict)
def add_funds(
    fund_update: FundUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add funds to user account"""
    if fund_update.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    funds = db.query(Fund).filter(Fund.user_id == current_user.user_id).first()
    
    if funds:
        funds.balance += fund_update.amount
    else:
        funds = Fund(user_id=current_user.user_id, balance=fund_update.amount)
        db.add(funds)
    
    db.commit()
    return {"message": "Funds added successfully"}

@router.post("/withdraw", response_model=dict)
def withdraw_funds(
    fund_update: FundUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Withdraw funds from user account"""
    if fund_update.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    funds = db.query(Fund).filter(Fund.user_id == current_user.user_id).first()
    
    if not funds or funds.balance < fund_update.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    funds.balance -= fund_update.amount
    db.commit()
    
    return {"message": "Withdrawal successful"}