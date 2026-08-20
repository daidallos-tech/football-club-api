from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from football_club_api.models import Teams, Player
from football_club_api.schemas import TeamCreateDTO, PlayerCreateDTO
from sqlalchemy import select, func
from collections.abc import Sequence 

from typing import List

class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_teams(self, teams_dto: List[TeamCreateDTO]) -> None:
        """Add football teams in your database"""
        for dto in teams_dto:
            # {"id": 57, "name": "Arsenal FC", "short_name": "Arsenal", "tla": "ARS"}
            insert_data = dto.model_dump(by_alias=False, exclude={"squad"})
            
            stmt = insert(Teams).values(**insert_data)
            
            stmt = stmt.on_conflict_do_update(
                index_elements=[Teams.id],
                set_={k: v for k, v in insert_data.items() if k != "id"}
            )
            
            await self.session.execute(stmt)
        
        await self.session.commit()

    async def upsert_players(self, players_dto: List[PlayerCreateDTO], team_id: int) -> None:
        """Add football players in your database"""
        for dto in players_dto:
            insert_data = dto.model_dump(by_alias=False)
            
            insert_data["team_id"] = team_id
            
            stmt = insert(Player).values(**insert_data)
            
            stmt = stmt.on_conflict_do_update(
                index_elements=[Player.id],
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

    async def get_team_by_team_id(self, team_id: int) -> Teams | None:
        result = await self.session.execute(
            select(Teams).where(Teams.id == team_id)
        )
        return result.scalars().first()

    async def get_teams_by_parameters_paginate(
            self,
            limit: int,
            offset: int,
            name: str | None = None,
            league: str | None = None,
            country: str | None = None
        ) -> tuple[Sequence[Teams], int]:
            query = select(Teams)
            
            count_query = select(func.count()).select_from(Teams)
    
            filters = []
            if name:
                filters.append(Teams.name == name)
            if league:
                filters.append(Teams.league_code == league)
            if country:
                filters.append(Teams.country == country)
    
            if filters:
                query = query.where(*filters)
                count_query = count_query.where(*filters)
    
            query = query.order_by(Teams.id.desc()).limit(limit).offset(offset)
    
            total_result = await self.session.execute(count_query)
            total = total_result.scalar_one()
    
            items_result = await self.session.execute(query)
            items = items_result.scalars().all()
    
            return items, total