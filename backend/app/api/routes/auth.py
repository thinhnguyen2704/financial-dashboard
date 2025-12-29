from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import Token
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.api.deps import get_db
from app.core.config import settings
from pydantic import BaseModel, EmailStr, Field
from jose import jwt

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

    new_user = User(email=data.email, hashed_password=hash_password(data.password))
    db.add(new_user)
    db.commit()

    return {"access_token": create_access_token(new_user.email)}


@router.post("/login")
def login(data: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "token_type": "bearer",
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh(data: RefreshRequest):
    payload = jwt.decode(
        data.refresh_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401)

    return {"access_token": create_access_token(payload["sub"])}
