from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship
from app.models.role import Role
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(Role), default=Role.user, nullable=False)
    hashed_password = Column(String, nullable=False)
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
    portfolios = relationship(
        "Portfolio", back_populates="user", cascade="all, delete-orphan"
    )
