from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user
from app.models.role import Role
from app.models.user import User

def require_role(required_role: Role):
    def role_dependency(
        user: User = Depends(get_current_user),
    ) -> User:
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_dependency