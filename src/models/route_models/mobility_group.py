from typing import Dict

from pydantic import BaseModel, Field


class NewMobilityGroup(BaseModel):
    identifier: str = Field(...)
    configuration: str = Field(...)
    distribution: Dict = Field(...)
    name: str = Field(...)
