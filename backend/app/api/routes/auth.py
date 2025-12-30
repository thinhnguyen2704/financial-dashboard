from fastapi import APIRouter, Depends, HTTPException, status, Body
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
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from app.models.refresh_token import RefreshToken
from app.models.role import Role

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

    return {"access_token": create_access_token(new_user.email)}


@router.post("/login")
def login(data: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_access_token({"sub": user.email, "role": user.role})

    refresh_token, expires = create_refresh_token()
    db.add(RefreshToken(token=refresh_token, user_id=user.id, expires_at=expires))
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(token: str = Body(...), db: Session = Depends(get_db)):
    stored = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token,
            not RefreshToken.revoked,
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )

    if not stored:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(
        {"sub": stored.user.email, "role": stored.user.role}
    )

    return {"access_token": access_token}
