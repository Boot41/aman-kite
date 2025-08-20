from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Holding(Base):
    __tablename__ = "holdings"

    holding_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.stock_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    average_cost = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="holdings")
    stock = relationship("Stock")