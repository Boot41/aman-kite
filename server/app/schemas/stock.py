from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class StockBase(BaseModel):
    ticker_symbol: str
    company_name: str
    current_price: float

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    stock_id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class StockSearchResponse(BaseModel):
    stock_id: int
    ticker_symbol: str
    company_name: str

    class Config:
        from_attributes = True

class StockDetailResponse(StockResponse):
    historical_data: Optional[dict] = None