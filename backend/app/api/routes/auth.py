from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.schemas.user import Token
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.db.session import get_db
from pydantic import BaseModel, EmailStr, Field
from app.models.refresh_token import RefreshToken
from app.models.role import Role
from app.schemas.token import TokenResponse
from app.core.config import settings

router = APIRouter()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


@router.post("/signup", response_model=Token)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if len(data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer",
        )

    is_user_existed = db.query(User).filter(User.email == data.email).first()
    if is_user_existed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    new_user = User(
        email=data.email, hashed_password=hash_password(data.password), role=Role.user
    )
    db.add(new_user)
    db.commit()

    return {
        "access_token": create_access_token(
            {
                "sub": new_user.email,
                "role": new_user.role,
            }
        )
    }


@router.post("/login")
def login(data: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token({"sub": user.email, "role": user.role})

    refresh_token = create_refresh_token({"sub": user.email})
    expires = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    db.add(RefreshToken(token=refresh_token, user_id=user.id, expires_at=expires))
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest):
    payload = decode_refresh_token(data.refresh_token)

    access_token = create_access_token(
        {
            "sub": payload["sub"],
            "role": "user",
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
