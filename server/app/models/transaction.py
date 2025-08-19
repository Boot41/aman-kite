from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.stock_id"), nullable=False)
    transaction_type = Column(String(4), nullable=False)  # 'BUY' or 'SELL'
    quantity = Column(Integer, nullable=False)
    price_per_share = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    stock = relationship("Stock")