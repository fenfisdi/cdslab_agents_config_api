from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from .distribution import NaturalDistribution


class NewNaturalHistory(BaseModel):
    vulnerability_group: UUID = Field(...)
    disease_group: UUID = Field(...)
    distribution: List[NaturalDistribution] = Field(...)
    avoidance_radius: float = Field(...)
    transitions: dict = Field(...)


class UpdateNaturalHistory(NewNaturalHistory):
    identifier: UUID = Field(...)
