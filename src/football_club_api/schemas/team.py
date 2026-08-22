from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from typing_extensions import Annotated
from pydantic.types import StringConstraints
from enum import Enum

CleanString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
ValidYear = Annotated[int, Field(ge=1500, le=2100)]

class PlayerPosition(str, Enum):
    GOALKEEPER = "Goalkeeper"
    DEFENDER = "Defence"
    MIDFIELDER = "Midfield"
    FORWARD = "Offence"

class PlayerBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    
    id: int
    name: CleanString
    position: PlayerPosition | None = None
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    nationality: CleanString | None = None

class PlayerCreateDTO(PlayerBase):
    pass
    
class PlayerResponse(PlayerBase):
    team_id: int

class PlayerUpdate(BaseModel):
    name: CleanString | None = None
    position: PlayerPosition | None = None
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    nationality: CleanString | None = None
    team_id: int | None = None

class PlayerCreate(BaseModel):
    name: CleanString
    position: PlayerPosition 
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    nationality: CleanString
    team_id: int


class TeamBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int 
    name: CleanString | None = None
    short_name: CleanString | None = Field(alias="shortName")
    tla: CleanString
    founded: ValidYear | None = None

class TeamCreate(BaseModel):
    name: CleanString 
    short_name: CleanString = Field(alias="shortName")
    tla: CleanString
    founded: ValidYear | None = None
    country: CleanString
    league_code: CleanString = Field(alias="leagueCode")

class TeamCreateDTO(TeamBase):
    country: CleanString
    league_code: CleanString
    squad: List[PlayerCreateDTO] = []

class TeamResponse(TeamBase):
    country: CleanString | None = None
    league_code: CleanString | None = Field(alias="leagueCode")

class TeamUpdate(BaseModel):
    name: CleanString | None = None
    short_name: CleanString | None = Field(default=None, alias="shortName")
    tla: CleanString | None = None
    founded: ValidYear | None = None
    country: CleanString | None = None
    league_code: CleanString | None = Field(default=None, alias="leagueCode")
