from fastapi import WebSocket, status
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User


async def get_current_user_ws(ws: WebSocket) -> User:
    token = ws.query_params.get("token")

    if not token:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("Missing token")

    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if not email:
            raise RuntimeError("Invalid token payload")
    except ExpiredSignatureError:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("TOKEN_EXPIRED")
    except JWTError:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("Invalid token")

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise RuntimeError("User not found")
        return user
    finally:
        db.close()
