from pydantic import BaseModel, Field

from .distribution import Distribution


class NewSusceptibilityGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(...)


class UpdateSusceptibilityGroup(NewSusceptibilityGroup):
    name: str = Field(None)
    distribution: Distribution = Field(None)
