from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from football_club_api.models import Teams
from football_club_api.schemas import TeamCreateDTO
from sqlalchemy import select
from collections.abc import Sequence 

from typing import List

class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_teams(self, teams_dto: List[TeamCreateDTO]) -> None:
        for dto in teams_dto:
            # {"id": 57, "name": "Arsenal FC", "short_name": "Arsenal", "tla": "ARS"}
            insert_data = dto.model_dump(by_alias=False)
            
            stmt = insert(Teams).values(**insert_data)
            
            stmt = stmt.on_conflict_do_update(
                index_elements=[Teams.id],
                set_={k: v for k, v in insert_data.items() if k != "id"}
            )
            
            await self.session.execute(stmt)
        
        await self.session.commit()

    async def get_teams_by_league(self, league_code: str) -> Sequence[Teams]:
        stmt = select(Teams).where(Teams.league_code == league_code)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_teams_by_country(self, country: str) -> Sequence[Teams]:
        stmt = select(Teams).where(Teams.country == country)
        result = await self.session.execute(stmt)
        return result.scalars().all()