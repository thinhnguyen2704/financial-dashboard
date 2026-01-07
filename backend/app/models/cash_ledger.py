from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class CashLedger(Base):
    __tablename__ = "cash_ledger"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(
        Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )

    amount = Column(Numeric(18, 8), nullable=False)
    reason = Column(String(16), nullable=False)
    reference_id = Column(Integer)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="cash_ledger")
