from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import TeamRepository
from football_club_api.services import TeamService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import TeamResponse, TeamCreate, TeamUpdate

router = APIRouter()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_team(
    team_data: TeamCreate, 
    current_admin: CurrentAdmin,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TeamResponse:
    """ Team creation """
    team_repository = TeamRepository(db)
    team_service = TeamService(team_repository)
    
    try:
        new_team = await team_service.create_team(team_data)
        return new_team
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{team_id}")
async def admin_partial_update_team_by_id(
    team_id: int,
    team_update: TeamUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
) -> TeamResponse:
    """Admin update user's profile information by their id"""
    team_repository = TeamRepository(db)
    team_service = TeamService(team_repository)

    try:
        updated_team = await team_service.admin_update_partial_team_by_id(
            team_id=team_id,
            team_update=team_update
        )
        return updated_team
    except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

@router.delete(
     "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_delete_team_by_id(
    team_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
):
    "Admin delete any team by its id"
    team_repository = TeamRepository(db)
    team_service = TeamService(team_repository)

    try:
        await team_service.admin_delete_team_by_id(team_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    