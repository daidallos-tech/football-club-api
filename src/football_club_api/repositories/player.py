from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from football_club_api import models
from football_club_api.models import Player
from football_club_api.schemas import PlayerCreateDTO
from sqlalchemy import select, func
from typing import Sequence

class PlayerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_player_by_player_id(self, player_id: int) -> Player | None:
        result = await self.session.execute(
            select(Player).where(Player.id == player_id)
        )
        return result.scalars().first()

    async def get_players_by_parameters_paginate(
        self,
        limit: int,
        offset: int,
        position: str | None = None,
        nationality: str | None = None
    ) -> tuple[Sequence[Player], int]:
        query = select(Player)
        
        count_query = select(func.count()).select_from(Player)

        filters = []
        if position:
            filters.append(Player.position == position)
        if nationality:
            filters.append(Player.nationality == nationality)

        if filters:
            query = query.where(*filters)
            count_query = count_query.where(*filters)

        query = query.order_by(Player.id.desc()).limit(limit).offset(offset)

        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        items_result = await self.session.execute(query)
        items = items_result.scalars().all()

        return items, total

    async def create_player(self, id: int, name: str, position: str, date_of_birth: date | None, nationality: str, team_id: int) -> Player:
    
        new_player = Player(
            id=id,
            name=name,
            position=position,
            date_of_birth=date_of_birth,
            nationality=nationality,
            team_id=team_id
        )

        self.session.add(new_player)
        await self.session.commit()
        await self.session.refresh(new_player)
        return new_player

    async def update_player(self, db_player: Player, update_data: dict) -> Player:
        for key, value in update_data.items():
            setattr(db_player, key, value) 

        self.session.add(db_player)
        await self.session.commit()
        await self.session.refresh(db_player)
        return db_player
    
    async def delete_player(self, db_team: Player) -> None:
        await self.session.delete(db_team)
        await self.session.commit()