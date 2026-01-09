from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    symbol = Column(String, nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    avg_price = Column(Numeric(18, 6), nullable=False)

    portfolio = relationship("Portfolio", back_populates="positions")
