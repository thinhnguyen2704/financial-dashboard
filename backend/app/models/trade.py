from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(
        Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )

    symbol = Column(String(32), nullable=False)
    side = Column(String(4), nullable=False)
    quantity = Column(Numeric(18, 8), nullable=False)
    price = Column(Numeric(18, 8), nullable=False)
    fee = Column(Numeric(18, 8), nullable=False, default=0)
    slippage = Column(Numeric(18, 8), nullable=False, default=0)

    executed_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    realized_pnl = Column(Numeric(18, 6), nullable=False)


    portfolio = relationship("Portfolio", back_populates="trades")

    __table_args__ = (
        CheckConstraint("side IN ('BUY', 'SELL')", name="ck_trade_side"),
        CheckConstraint("quantity > 0", name="ck_trade_quantity"),
        CheckConstraint("price >= 0", name="ck_trade_price"),
    )
