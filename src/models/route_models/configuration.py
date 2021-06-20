from datetime import datetime

from pydantic import BaseModel, Field

from src.models.general import UnitLength, UnitTime


class IntervalDate(BaseModel):
    start: datetime = Field(...)
    end: datetime = Field(...)


class UpdateConfiguration(BaseModel):
    name: str = Field(None)
    population_number: int = Field(None)
    interval_date: IntervalDate = Field(None)
    iteration_time_units: UnitTime = Field(None)
    iteration_number: int = Field(None)
    box_size: dict = Field(None)
    distance_units: UnitLength = Field(None)


class NewConfiguration(UpdateConfiguration):
    name: str = Field(...)
    population_number: int = Field(...)
    interval_date: IntervalDate = Field(...)
    iteration_time_units: UnitTime = Field(...)
    iteration_number: int = Field(...)
    box_size: dict = Field(...)
    distance_units: UnitLength = Field(...)
