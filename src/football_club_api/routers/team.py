from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import TeamRepository
from football_club_api.services import TeamService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import TeamResponse


router = APIRouter()

@router.get("/{team_id}", status_code=status.HTTP_200_OK)
async def get_team_by_id(
    team_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TeamResponse:
    team_repository = TeamRepository(db)
    team_service = TeamService(team_repository)

    try:
        team = await team_service.get_team_by_id(team_id)
        return team
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )