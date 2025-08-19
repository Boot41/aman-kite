from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Fund(Base):
    __tablename__ = "funds"

    fund_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0.00)
    
    # Relationship
    user = relationship("User")