from typing import Dict

from pydantic import BaseModel, Field

from src.models.general import DiseaseDistributionType, UnitLength
from .distribution import Distribution


class UpdateDiseaseGroup(BaseModel):
    name: str = Field(None)
    can_infected: bool = Field(None)
    is_infected: bool = Field(None)
    can_spread: bool = Field(None)
    spread_radius: float = Field(None)
    spread_radius_unit: UnitLength = Field(None)
    spread_probability: float = Field(None)
    distributions: Dict[DiseaseDistributionType, Distribution] = Field(None)

    class Config:
        use_enum_values = True


class NewDiseaseGroup(UpdateDiseaseGroup):
    name: str = Field(...)
    # distributions: List[DiseaseDistribution] = Field(...)
