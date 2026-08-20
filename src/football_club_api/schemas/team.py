from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class PlayerBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    
    id: int
    name: str
    position: Optional[str] = None
    date_of_birth: Optional[date] = Field(None, alias="dateOfBirth")
    nationality: Optional[str] = None

class PlayerCreateDTO(PlayerBase):
    pass
    
class PlayerResponse(PlayerBase):
    team_id: int

class TeamBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int 
    name: str
    short_name: str = Field(alias="shortName")
    tla: str
    founded: Optional[int] = None

class TeamCreateDTO(TeamBase):
    country: str
    league_code: str
    squad: List[PlayerCreateDTO] = []

class TeamResponse(TeamBase):
    country: str
    league_code: str

