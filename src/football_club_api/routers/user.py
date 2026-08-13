from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.schemas import UserCreate, UserPrivate, UserPublic
from football_club_api.repositories.user import UserRepository
from football_club_api.services.auth import AuthService, UserService

router = APIRouter()

@router.post(
    "",
    response_model=UserPrivate,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """ User creation """
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)
    
    try:
        new_user = await auth_service.register_user(user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_user_id(
    user_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """ Get user profile by user id """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        user = await user_service.get_user_profile_by_id(user_id)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
