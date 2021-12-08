from pydantic import BaseModel, Field

from .distribution import Distribution


class NewMobilityGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(None)


class UpdateMobilityGroup(BaseModel):
    name: str = Field(None)
    distribution: Distribution = Field(None)
