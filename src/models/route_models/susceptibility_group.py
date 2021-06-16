from pydantic import BaseModel, Field


class NewSusceptibilityGroup(BaseModel):
    identifier: str = Field(...)
    configuration: str = Field(...)
    distribution: str = Field(...)
    name: str = Field(...)
