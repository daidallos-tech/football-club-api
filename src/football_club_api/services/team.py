from football_club_api.clients import FootballDataClient
from football_club_api.repositories import TeamRepository
from football_club_api.schemas import TeamCreateDTO

class TeamSyncService:
    def __init__(self, api_client: FootballDataClient, team_repo: TeamRepository):
        self.api_client = api_client
        self.team_repo = team_repo

    async def sync_teams(self, league_code: str, country: str) -> None:
        raw_data = await self.api_client.fetch_raw_league_teams(league_code)
        raw_teams = raw_data.get("teams", [])

        teams_dto = []
        for team_json in raw_teams:
            team_json["country"] = country
            team_json["league_code"] = league_code
            
            dto = TeamCreateDTO(**team_json)
            teams_dto.append(dto)

        await self.team_repo.upsert_teams(teams_dto)