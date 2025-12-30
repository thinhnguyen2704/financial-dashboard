import enum


class Role(str, enum.Enum):
    user = "user"
    admin = "admin"
