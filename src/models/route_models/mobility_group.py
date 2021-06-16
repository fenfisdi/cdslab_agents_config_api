from pydantic import BaseModel, Field

from .distribution import NewDistribution


class NewMobilityGroup(BaseModel):
    distribution: NewDistribution = Field(...)
    name: str = Field(...)
