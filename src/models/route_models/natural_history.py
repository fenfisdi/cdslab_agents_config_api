from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.general import UnitLength
from .distribution import NaturalDistribution


class UpdateNaturalHistory(BaseModel):
    distribution: List[NaturalDistribution] = Field(None)
    avoidance_radius: float = Field(None)
    transitions: dict = Field(None)


class NewNaturalHistory(UpdateNaturalHistory):
    vulnerability_group: UUID = Field(...)
    disease_group: UUID = Field(...)
    distribution: List[NaturalDistribution] = Field(...)
    avoidance_radius: float = Field(...)
    avoidance_radius_unit: UnitLength = Field(...)
    transitions: dict = Field(...)
