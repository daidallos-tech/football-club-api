from fastapi import APIRouter

from .user import router as user_router
from .admin import router as admin_router
from .team import router as team_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix="/users", tags=["Users"])

api_router.include_router(admin_router, prefix="/admin", tags=["Admins"])

api_router.include_router(team_router, prefix="/teams", tags=["Teams"])

__all__ = ["api_router"]