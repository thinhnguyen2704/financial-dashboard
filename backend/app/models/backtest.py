from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Backtest(Base):
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    initial_cash = Column(Float, nullable=False)
    final_equity = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    runs = relationship(
        "BacktestRun",
        back_populates="backtest",
        cascade="all, delete-orphan",
    )


class BacktestTrade(Base):
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True)
    backtest_id = Column(
        Integer,
        ForeignKey("backtests.id", ondelete="CASCADE"),
        nullable=False,
    )

    timestamp = Column(DateTime(timezone=True), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)

    quantity = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    fee = Column(Numeric(20, 8), nullable=False)
    slippage = Column(Numeric(20, 8), nullable=False)

    realized_pnl = Column(Numeric(20, 8), nullable=False)

    backtest = relationship("Backtest", back_populates="trades")

    __table_args__ = (Index("ix_backtest_trade_backtest_id", "backtest_id"),)

class BacktestEquity(Base):
    __tablename__ = "backtest_equity"

    id = Column(Integer, primary_key=True)
    backtest_id = Column(
        Integer,
        ForeignKey("backtests.id", ondelete="CASCADE"),
        nullable=False,
    )

    timestamp = Column(DateTime(timezone=True), nullable=False)
    equity = Column(Numeric(20, 8), nullable=False)
    cash = Column(Numeric(20, 8), nullable=False)

    backtest = relationship("Backtest", back_populates="equity_curve")

    __table_args__ = (
        Index("ix_backtest_equity_backtest_id", "backtest_id"),
        Index("ix_backtest_equity_timestamp", "timestamp"),
    )
