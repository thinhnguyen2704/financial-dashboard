from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
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
