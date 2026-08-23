from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from football_club_api.db import get_db
from football_club_api.repositories import PlayerRepository, TeamRepository
from football_club_api.services import PlayerService
from football_club_api.security import CurrentAdmin
from football_club_api.schemas import PlayerResponse, PlayerUpdate, PlayerCreate

router = APIRouter()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_player(
    player_data: PlayerCreate, 
    current_admin: CurrentAdmin,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> PlayerResponse:
    """Player creation by Admin"""
    player_repository = PlayerRepository(db)
    team_repository = TeamRepository(db)
    player_service = PlayerService(player_repository, team_repository)
    
    try:
        new_player = await player_service.create_player(player_data)
        return new_player
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{player_id}")
async def admin_partial_update_player_by_id(
    player_id: int,
    player_update: PlayerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
) -> PlayerResponse:
    """Player profile udpate information by their id by Admin"""
    team_repository = TeamRepository(db)
    palyer_repository = PlayerRepository(db)
    player_service = PlayerService(palyer_repository, team_repository)

    try:
        updated_player = await player_service.admin_update_partial_player_by_id(player_id, player_update)
        return updated_player
    except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

@router.delete(
     "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_delete_player_by_id(
    player_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_admin: CurrentAdmin,
):
    """Delete player by their id by Admin"""
    player_repository = PlayerRepository(db)
    team_repository = TeamRepository(db)
    player_service = PlayerService(player_repository, team_repository)

    try:
        await player_service.admin_delete_player_by_id(player_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )