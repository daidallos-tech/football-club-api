from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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

class TeamResponse(TeamBase):
    country: str