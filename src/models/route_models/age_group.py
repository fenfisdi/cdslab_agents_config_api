from pydantic import BaseModel, Field


class NewAgeGroup(BaseModel):
    identifier: str = Field(...)
    configuration: str = Field(...)
    name: str = Field(...)
    population_percentage: float = Field(...)
