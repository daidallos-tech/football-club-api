from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.schemas import UserCreate, UserPrivate, UserPublic, UserUpdate
from football_club_api.repositories.user import UserRepository
from football_club_api.services import AuthService, UserService
from football_club_api.models import Token
from football_club_api.security import CurrentUser


router = APIRouter()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserPrivate:
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

@router.get("/me")
async def get_current_user(
    current_user: CurrentUser
) -> UserPrivate:
    """ Get current authorized user """
    return UserPrivate.model_validate(current_user) 

@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def get_user_by_user_id(
    user_id: int, 
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserPublic:
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

@router.post("/token")
async def access_by_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> Token:
    user_repository = UserRepository(db)
    auth_service = AuthService(user_repository)

    login_input = form_data.username.strip().lower()

    try:
        return await auth_service.authenticate_user(
            login_input=login_input, 
            password_input=form_data.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.patch("/me")
async def partial_user_profile_update(
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
) -> UserPrivate:
    """User's profile partial UPDATE """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        update_user = await user_service.partial_update_user_profile(
            current_user=current_user,
            user_update=user_update
        )
        return update_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """ Delete current user """
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    try:
        await user_service.delete_user(current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )