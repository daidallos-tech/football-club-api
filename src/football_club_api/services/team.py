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

        await self.team_repo.upsert_teams(teams_dto)

    async def get_team_by_id(self, team_id: int) -> TeamResponse:
        team = await self.team_repo.get_team_by_team_id(team_id)
        
        if not team:
            raise ValueError("Team not found")
            
        return TeamResponse.model_validate(team)