from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from .distribution import Distribution


class NewNaturalHistory(BaseModel):
    vulnerability_group: UUID = Field(...)
    disease_state: UUID = Field(...)
    configuration: UUID = Field(...)
    distribution: List[Distribution] = Field(...)
    avoidance_radius: float = Field(...)
    transitions: dict = Field(...)


class UpdateNaturalHistory(NewNaturalHistory):
    identifier: UUID = Field(...)
