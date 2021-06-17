from pydantic import BaseModel, Field

from src.models import NewDistribution


class NewSusceptibilityGroup(BaseModel):
    distribution: NewDistribution = Field(...)
    name: str = Field(...)
