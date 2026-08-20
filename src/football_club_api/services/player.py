from football_club_api.repositories import PlayerRepository
from football_club_api.schemas import PlayerResponse

class PlayerService:
    def __init__(self, player_repo: PlayerRepository):
            self.player_repo = player_repo
    
    async def get_player_by_player_id(self, player_id: int) -> PlayerResponse:
        player = await self.player_repo.get_player_by_player_id(player_id)
        
        if not player:
            raise ValueError("Player not found")
            
        return PlayerResponse.model_validate(player)

    async def get_players_catalog(
        self,
        limit: int,
        offset: int,
        position: str | None = None,
        nationality: str | None = None
    ) -> tuple[list[PlayerResponse], int]:
        if position:
            position = position.strip()
            
            ALLOWED_POSITIONS = {"Goalkeeper", "Defender", "Midfielder", "Forward"}
            if position.capitalize() not in ALLOWED_POSITIONS:
                raise ValueError(f"Invalid position: {position}")

        if nationality:
            nationality = nationality.strip()
            if len(nationality) < 2:
                raise ValueError("Nationality name is too short")
        
        items, total = await self.player_repo.get_players_by_parameters_paginate(
            limit=limit,
            offset=offset,
            position=position,
            nationality=nationality
        )

        validated_items = [PlayerResponse.model_validate(player) for player in items]

        return validated_items, total
              