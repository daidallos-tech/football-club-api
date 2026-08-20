from football_club_api.clients import FootballDataClient
from football_club_api.repositories import TeamRepository
from football_club_api.schemas import TeamCreateDTO, TeamResponse

class TeamService:
    def __init__(self, team_repo: TeamRepository, api_client: FootballDataClient | None = None):
        self.api_client = api_client
        self.team_repo = team_repo

    async def sync_teams(self, league_code: str, country: str) -> None:

        if self.api_client is None:
            raise RuntimeError("API client is not initialized.")
        
        raw_data = await self.api_client.fetch_raw_league_teams(league_code)
        raw_teams = raw_data.get("teams", [])

        teams_dto = []
        for team_json in raw_teams:
            team_json["country"] = country
            team_json["league_code"] = league_code
            
            dto = TeamCreateDTO(**team_json)
            teams_dto.append(dto)

        print(f"Writing teams {league_code}...")
        await self.team_repo.upsert_teams(teams_dto)

        print(f"Uploading team players in PostgreSQL...")
        for team_dto in teams_dto:
            if team_dto.squad:
                await self.team_repo.upsert_players(players_dto=team_dto.squad, team_id=team_dto.id)
                
        print(f"Synchronization was successfully done!")

    async def get_team_by_id(self, team_id: int) -> TeamResponse:
        team = await self.team_repo.get_team_by_team_id(team_id)
        
        if not team:
            raise ValueError("Team not found")
            
        return TeamResponse.model_validate(team)

    async def get_teams_catalog(
            self,
            limit: int,
            offset: int,
            leauge: str | None = None,
            country: str | None = None
        ) -> tuple[list[TeamResponse], int]:
            
            items, total = await self.team_repo.get_teams_by_parameters_paginate(
                limit=limit,
                offset=offset,
                league=leauge,
                country=country
            )
    
            validated_items = [TeamResponse.model_validate(team) for team in items]
    
            return validated_items, total