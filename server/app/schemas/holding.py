from pydantic import BaseModel
from typing import Optional

class HoldingBase(BaseModel):
    stock_id: int
    quantity: int
    average_cost: float

class HoldingCreate(HoldingBase):
    pass

class HoldingResponse(HoldingBase):
    holding_id: int
    user_id: int
    ticker_symbol: Optional[str] = None
    current_price: Optional[float] = None
    total_value: Optional[float] = None
    profit_loss: Optional[float] = None

    class Config:
        from_attributes = True