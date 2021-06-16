from pydantic import BaseModel, Field


class NewAgeGroup(BaseModel):
    configuration: str = Field(...)
    name: str = Field(...)
    population_percentage: float = Field(...)
