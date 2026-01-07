from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from app.core.config import settings
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.user import User
import bcrypt

MAX_BCRYPT_BYTES = 72
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


def _validate_password_bytes(password: str) -> None:
    if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 bytes or fewer",
        )


def hash_password(password: str) -> str:
    _validate_password_bytes(password)

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    _validate_password_bytes(password)

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(data: dict):
    to_encode = data.copy()

    if not isinstance(to_encode.get("sub"), str):
        raise ValueError("JWT sub must be a string")

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        raise
    except JWTError:
        raise


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def create_refresh_token(data: dict) -> str:
    if not isinstance(data.get("sub"), str):
        raise ValueError("JWT sub must be a string")

    print("REFRESH DAYS:", settings.REFRESH_TOKEN_EXPIRE_DAYS)

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode = {
        "sub": data["sub"],
        "exp": expire,
        "type": "refresh",
    }

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        raise RuntimeError("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise RuntimeError("Invalid refresh token type")

    sub = payload.get("sub")
    if not isinstance(sub, str):
        raise RuntimeError("Invalid refresh token subject")

    return payload
