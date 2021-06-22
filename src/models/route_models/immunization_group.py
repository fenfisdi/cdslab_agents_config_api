from pydantic import BaseModel, Field

from src.models import Distribution


class NewImmunizationGroup(BaseModel):
    name: str = Field(...)
    distribution: Distribution = Field(...)
