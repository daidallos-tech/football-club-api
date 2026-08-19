import httpx
from typing import Dict, Any

class FootballDataClient:
    def __init__(self, api_token: str, base_url: str = "https://api.football-data.org/v4/"):
        self.base_url = base_url
        self.headers = {"X-Auth-Token": api_token}

    async def fetch_raw_league_teams(self, league_code: str = "PL") -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as client:
            response = await client.get(f"/competitions/{league_code}/teams")
            response.raise_for_status()
            return response.json()