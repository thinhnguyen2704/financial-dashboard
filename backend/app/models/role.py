from sqlalchemy import Column, Enum
import enum

class Role(str, enum.Enum):
    user = "user"
    admin = "admin"

role = Column(Enum(Role), default=Role.user)
