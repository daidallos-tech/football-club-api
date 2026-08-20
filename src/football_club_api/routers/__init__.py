from fastapi import APIRouter

from .user import router as user_router
from .admin import router as admin_router
from .team import router as team_router
from .player import router as player_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix="/users", tags=["Users"])

api_router.include_router(admin_router, prefix="/admin/users", tags=["Admins"])

api_router.include_router(team_router, prefix="/teams", tags=["Teams"])

api_router.include_router(player_router, prefix="/players", tags=["Players"])

__all__ = ["api_router"]