from pydantic import BaseModel

class FundBase(BaseModel):
    balance: float

class FundResponse(FundBase):
    user_id: int

    class Config:
        from_attributes = True

class FundUpdate(BaseModel):
    amount: float