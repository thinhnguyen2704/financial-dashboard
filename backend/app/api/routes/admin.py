from fastapi import APIRouter, Depends
from app.models.user import User
from app.models.role import Role
from app.core.deps import require_role

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def admin_stats(
    user: User = Depends(require_role(Role.admin)),
):
    return {"status": "ok"}
