from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String)
    side = Column(String)  # BUY / SELL
    quantity = Column(Float)
    price = Column(Float)
    fee = Column(Float)
    slippage = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    portfolio = relationship("Portfolio", back_populates="trades")

