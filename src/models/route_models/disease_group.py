from typing import List

from pydantic import BaseModel, Field

from .distribution import DiseaseDistribution


class NewDiseaseGroup(BaseModel):
    name: str = Field(...)
    can_infected: bool = Field(...)
    is_infected: bool = Field(...)
    can_spread: bool = Field(...)
    spread_radius: float = Field(None)
    spread_probability: float = Field(None)
    distributions: List[DiseaseDistribution] = Field(...)
