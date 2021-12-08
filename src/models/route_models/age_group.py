from pydantic import BaseModel, Field


class UpdateAgeGroup(BaseModel):
    name: str = Field(None)
    population_percentage: float = Field(None)


class NewAgeGroup(UpdateAgeGroup):
    name: str = Field(...)
    population_percentage: float = Field(...)
