from pydantic import BaseModel, Field

from .distribution import Distribution


class NewMobilityGroup(BaseModel):
    distribution: Distribution = Field(None)
    name: str = Field(...)
