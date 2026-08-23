from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import PlayerRepository, TeamRepository
from football_club_api.services import PlayerService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import PlayerResponse

from fastapi_pagination import LimitOffsetPage, LimitOffsetParams

router = APIRouter()

async def get_player_service(db: Annotated[AsyncSession, Depends(get_db)]) -> PlayerService:
    team_repo = TeamRepository(db)
    repo = PlayerRepository(db)
    return PlayerService(repo, team_repo) 

@router.get("/", response_model=LimitOffsetPage[PlayerResponse])
async def get_players_catalog(
    service: Annotated[PlayerService, Depends(get_player_service)],
    pagination: Annotated[LimitOffsetParams, Depends()], 
    position: str | None = None,                         
    nationality: str | None = None                       
):
    try:
        items, total = await service.get_players_catalog(
            limit=pagination.limit,
            offset=pagination.offset,
            position=position,
            nationality=nationality
        )
        
        return LimitOffsetPage.create(
            items=items,
            total=total,
            params=pagination
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{player_id}", status_code=status.HTTP_200_OK)
async def get_player_by_player_id(
    player_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> PlayerResponse:
    team_repo = TeamRepository(db)
    player_repository = PlayerRepository(db)
    player_service = PlayerService(player_repository, team_repo)

    try:
        player = await player_service.get_player_by_player_id(player_id)
        return player
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

