from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login():
    # Placeholder (DB logic next phase)
    token = create_access_token("user@example.com")
    return {"access_token": token, "token_type": "bearer"}
