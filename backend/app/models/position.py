from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.base import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    symbol = Column(String)
    quantity = Column(Float)
    avg_price = Column(Float)
