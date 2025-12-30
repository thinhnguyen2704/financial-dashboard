from typing import Optional
from fastapi import WebSocket, status
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User
from backend.app.models.role import Role


async def get_current_user_ws(
    ws: WebSocket,
    required_role: Optional[Role] = None,
) -> User:
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

    email = payload.get("sub")
    if not email:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("Invalid payload")

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            raise RuntimeError("User not found")

        if required_role and user.role != required_role:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            raise RuntimeError("Insufficient role")

        return user
    finally:
        db.close()
