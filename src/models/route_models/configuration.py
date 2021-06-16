from typing import Dict

from pydantic import BaseModel, Field


class NewConfiguration(BaseModel):
    name: str = Field(...)
    population_number: int = Field(...)
    interval_date: Dict = Field(...)
    iteration_time_units: str = Field(...)
    iteration_number: int = Field(...)
    box_size: Dict = Field(...)
    distance_units: str = Field(...)


class UpdateConfiguration(NewConfiguration):
    identifier: str = Field(...)
    is_delete: bool = Field(...)

