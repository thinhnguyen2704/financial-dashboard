from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    name = Column(String(255), nullable=False)
    base_currency = Column(String(8), nullable=False, default="USD")
    initial_cash = Column(Numeric(18, 2), nullable=False, default=100000)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="portfolios")
    trades = relationship(
        "Trade", back_populates="portfolio", cascade="all, delete-orphan"
    )
    positions = relationship(
        "Position",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    cash_ledger = relationship(
        "CashLedger", back_populates="portfolio", cascade="all, delete-orphan"
    )
