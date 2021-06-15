from pydantic import BaseModel, Field


class NewMobilityGroup(BaseModel):
    identifier: str = Field(...)
    configuration: str = Field(...)
    distribution: str = Field(...)
    name: str = Field(...)
