from typing import Dict
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.general import NaturalDistributionType, UnitLength
from .distribution import Distribution


class UpdateNaturalHistory(BaseModel):
    vulnerability_group: UUID = Field(...)
    disease_group: UUID = Field(...)
    distributions: Dict[NaturalDistributionType, Distribution] = Field(None)
    avoidance_radius: float = Field(None)
    transition_by_contagion: bool = Field(None)
    avoidance_radius_unit: UnitLength = Field(None)
