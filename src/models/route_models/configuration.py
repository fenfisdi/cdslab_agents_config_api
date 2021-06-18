from pydantic import BaseModel, Field


class UpdateConfiguration(BaseModel):
    name: str = Field(None)
    population_number: int = Field(None)


class NewConfiguration(UpdateConfiguration):
    name: str = Field(...)
    population_number: int = Field(...)
    interval_date: dict = Field(...)
    iteration_time_units: str = Field(...)
    iteration_number: int = Field(...)
    box_size: dict = Field(...)
    distance_units: str = Field(...)
