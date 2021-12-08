from pydantic import BaseModel, Field

from .distribution import Distribution


class NewImmunizationGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(...)
