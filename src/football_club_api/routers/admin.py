from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import UserRepository
from football_club_api.services import UserService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import UserUpdate, UserPrivate


router = APIRouter()

@router.delete("/admin/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user_by_id(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        await user_service.admin_delete_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.patch("/admin/{user_id}")
async def admin_partial_update_user_profile_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
) -> UserPrivate:
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        updated_user = await user_service.admin_update_partial_user_profile_by_id(
            user_id=user_id,
            user_update=user_update
        )
        return updated_user
    except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    