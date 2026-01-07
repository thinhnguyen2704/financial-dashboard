from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String, index=True)
    quantity = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    portfolio = relationship("Portfolio", back_populates="positions")
