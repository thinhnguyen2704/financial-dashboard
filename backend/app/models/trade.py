from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # BUY / SELL
    quantity = Column(Numeric(18, 6), nullable=False)
    price = Column(Numeric(18, 6), nullable=False)
    fee = Column(Numeric(18, 6), nullable=False)
    slippage = Column(Numeric(18, 6), nullable=False)

    realized_pnl = Column(Numeric(18, 6), nullable=False)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="trades")

    def to_event_dict(self) -> dict:
        return {
            "trade_id": self.id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "side": self.side,
            "quantity": str(self.quantity),
            "price": str(self.price),
            "fee": str(self.fee),
            "slippage": str(self.slippage),
            "realized_pnl": str(self.realized_pnl),
            "timestamp": self.timestamp.isoformat(),
        }
