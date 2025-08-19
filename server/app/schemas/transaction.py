from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    stock_id: int
    transaction_type: str
    quantity: int
    price_per_share: float

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: int
    user_id: int
    transaction_date: datetime
    ticker_symbol: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True