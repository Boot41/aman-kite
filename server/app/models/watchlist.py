from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    watchlist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.stock_id"), nullable=False)
    
    # Ensure a user can't add the same stock to watchlist multiple times
    __table_args__ = (UniqueConstraint('user_id', 'stock_id', name='_user_stock_uc'),)
    
    # Relationships
    user = relationship("User")
    stock = relationship("Stock")