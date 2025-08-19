from pydantic import BaseModel
from typing import Optional

class WatchlistBase(BaseModel):
    stock_id: int

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistResponse(WatchlistBase):
    watchlist_id: int
    user_id: int
    ticker_symbol: Optional[str] = None
    company_name: Optional[str] = None
    current_price: Optional[float] = None

    class Config:
        from_attributes = True