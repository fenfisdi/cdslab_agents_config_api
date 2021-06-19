from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from .distribution import NewDistribution


class NewNaturalHistory(BaseModel):
    vulnerability_group: UUID = Field(...)
    disease_state: UUID = Field(...)
    configuration: UUID = Field(...)
    distribution: List[NewDistribution] = Field(...)
    avodance_radius: float = Field(...)
    transitions: dict = Field(...)


class UpdateNaturalHistory(NewNaturalHistory):
    identifier: UUID = Field(...)
