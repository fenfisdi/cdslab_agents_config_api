from pydantic import BaseModel, Field

from src.models import NewDistribution


class NewImmunizationGroup(BaseModel):
    name: str = Field(...)
    distribution: NewDistribution = Field(...)
