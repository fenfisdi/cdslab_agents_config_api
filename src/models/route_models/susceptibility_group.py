from pydantic import BaseModel, Field

from src.models import Distribution


class NewSusceptibilityGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(...)
