from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.watchlist import Watchlist
from app.models.stock import Stock
from app.schemas.watchlist import WatchlistResponse, WatchlistCreate
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[WatchlistResponse])
def get_user_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's watchlist"""
    watchlist_items = (
        db.query(
            Watchlist.watchlist_id,
            Watchlist.user_id,
            Watchlist.stock_id,
            Stock.ticker_symbol,
            Stock.company_name,
            Stock.current_price
        )
        .join(Stock, Watchlist.stock_id == Stock.stock_id)
        .filter(Watchlist.user_id == current_user.user_id)
        .all()
    )
    
    response = []
    for item in watchlist_items:
        response.append(WatchlistResponse(
            watchlist_id=item.watchlist_id,
            user_id=item.user_id,
            stock_id=item.stock_id,
            ticker_symbol=item.ticker_symbol,
            company_name=item.company_name,
            current_price=float(item.current_price)
        ))
    
    return response

@router.post("/", response_model=dict)
def add_to_watchlist(
    watchlist_item: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add stock to user's watchlist"""
    # Check if stock exists
    stock = db.query(Stock).filter(Stock.stock_id == watchlist_item.stock_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Check if already in watchlist
    existing_item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.stock_id == watchlist_item.stock_id
    ).first()
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Stock already in watchlist")
    
    # Add to watchlist
    new_item = Watchlist(
        user_id=current_user.user_id,
        stock_id=watchlist_item.stock_id
    )
    db.add(new_item)
    db.commit()
    
    return {"message": "Stock added to watchlist"}

@router.delete("/{stock_id}", response_model=dict)
def remove_from_watchlist(
    stock_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove stock from user's watchlist"""
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.stock_id == stock_id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")
    
    db.delete(watchlist_item)
    db.commit()
    
    return {"message": "Stock removed from watchlist"}