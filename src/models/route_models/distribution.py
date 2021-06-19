from uuid import UUID

from pydantic import BaseModel, Field


class NewDistribution(BaseModel):
    identifier: UUID = Field(...)
    name: str = Field(...)
    distribution_type: str = Field(...)
    distribution_name: str = Field(...)
    distribution_filename: str = Field(...)
    distribution_extra_arguments: dict = Field(...)
