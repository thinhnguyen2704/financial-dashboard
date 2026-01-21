from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True)
    backtest_id = Column(Integer, ForeignKey("backtests.id"))

    timestamp = Column(DateTime, nullable=False)
    equity = Column(Float, nullable=False)

    backtest = relationship("Backtest", back_populates="runs")
