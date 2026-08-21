from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import TeamRepository
from football_club_api.services import TeamService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import TeamResponse, TeamCreate

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

