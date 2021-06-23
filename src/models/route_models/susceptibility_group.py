from pydantic import BaseModel, Field

from .distribution import Distribution


class NewSusceptibilityGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(...)
