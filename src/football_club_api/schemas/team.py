from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TeamCreateDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int 
    name: str
    short_name: str = Field(alias="shortName")
    tla: str
    founded: Optional[int] = None
    country: str
    league_code: str
