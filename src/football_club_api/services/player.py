import random
from football_club_api.repositories import PlayerRepository, TeamRepository
from football_club_api.schemas import PlayerResponse, PlayerCreate, PlayerPosition, PlayerUpdate

class PlayerService:
    def __init__(self, player_repo: PlayerRepository, team_repo: TeamRepository):
            self.player_repo = player_repo
            self.team_repo = team_repo
    
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
            position = position.strip().capitalize()
            if position not in [pos.value for pos in PlayerPosition]:
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

    async def create_player(
        self,
        player_data: PlayerCreate
    ) -> PlayerResponse:

        existing_team = await self.team_repo.get_team_by_team_id(player_data.team_id)
        if not existing_team:
           raise ValueError("Team doesn't exist") 
        
        admin_id = random.randint(10_000_000, 99_000_000)

        db_player = await self.player_repo.create_player(
            id=admin_id,
            name=player_data.name,
            position=player_data.position.value,
            date_of_birth=player_data.date_of_birth,
            nationality=player_data.nationality,
            team_id=player_data.team_id
        )

        return PlayerResponse.model_validate(db_player)

    async def admin_update_partial_player_by_id(self, player_id: int, player_update: PlayerUpdate) -> PlayerResponse:
        db_player = await self.player_repo.get_player_by_player_id(player_id)
        if not db_player:
            raise ValueError(f"Player with ID {player_id} not found")

        update_data = player_update.model_dump(exclude_unset=True)

        if "team_id" in update_data and update_data["team_id"] is not None:
            new_team_id = update_data["team_id"]
            new_team = await self.team_repo.get_team_by_team_id(new_team_id)
            if not new_team:
                raise ValueError(f"Target transfer Team with ID {new_team_id} does not exist")

        if "position" in update_data and update_data["position"] is not None:
            update_data["position"] = update_data["position"].value

        updated_db_player = await self.player_repo.update_player(db_player, update_data)
        
        return PlayerResponse.model_validate(updated_db_player)
    
    async def admin_delete_player_by_id(self, player_id: int) -> None:
        db_player = await self.player_repo.get_player_by_player_id(player_id)
        
        if not db_player:
            raise ValueError(f"Player with ID {player_id} not found")
    
        await self.player_repo.delete_player(db_player)
              