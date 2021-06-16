from pydantic import BaseModel, Field


class NewAgeGroup(BaseModel):
    name: str = Field(...)
    population_percentage: float = Field(...)
