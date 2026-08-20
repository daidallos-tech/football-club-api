from typing import TYPE_CHECKING

from datetime import date
from football_club_api.db import Base
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .teams import Teams

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    nationality: Mapped[str] = mapped_column(String(100))

    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), index=True)
    team: Mapped["Teams"] = relationship("Teams", backref="players_list")


