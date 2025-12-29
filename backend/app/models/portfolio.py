from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cash = Column(Float, default=10000)
