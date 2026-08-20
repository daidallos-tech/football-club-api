from football_club_api.db import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import CITEXT

class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(CITEXT(100), index=True)
    short_name: Mapped[str] = mapped_column(String(50))
    tla: Mapped[str] = mapped_column(String(10))
    founded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    country: Mapped[str] = mapped_column(CITEXT(50), index=True)
    league_code: Mapped[str] = mapped_column(CITEXT(10), index=True)
