import asyncio
from football_club_api.db import settings            
from football_club_api.clients import FootballDataClient
from football_club_api.db import AsyncSessionLocal
from football_club_api.repositories import TeamRepository
from football_club_api.services import TeamService

async def main():
    api_client = FootballDataClient(api_token=settings.FOOTBALL_API_TOKEN)

    async with AsyncSessionLocal() as session:
        team_repo = TeamRepository(session=session)
        
        sync_service = TeamService(api_client=api_client, team_repo=team_repo)

        print("Synchronization...")
        await sync_service.sync_teams(league_code="PL", country="England")
        #await sync_service.sync_teams(league_code="PD", country="Spain")
        print("Date was added successfully in PostgreSQL!")

if __name__ == "__main__":
    asyncio.run(main())
