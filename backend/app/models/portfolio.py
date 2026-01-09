from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)

    cash = Column(Numeric(18, 6), nullable=False)
    realized_pnl = Column(Numeric(18, 6), nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    positions = relationship(
        "Position", back_populates="portfolio", cascade="all, delete-orphan"
    )
    trades = relationship(
        "Trade", back_populates="portfolio", cascade="all, delete-orphan"
    )
