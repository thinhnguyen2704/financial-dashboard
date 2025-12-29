from fastapi import Depends, HTTPException
from app.models.role import Role 
from app.models.user import User
from app.core.security import get_current_user

def require_role(role: Role):
    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403)
        return user
    return checker
