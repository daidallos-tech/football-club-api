from fastapi import APIRouter

from .user import router as user_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix="/users", tags=["Users"])

__all__ = ["api_router"]