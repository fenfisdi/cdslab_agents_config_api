from pydantic import BaseModel, Field

from src.models.general import (
    DiseaseDistributionType,
    DistributionType,
    NaturalDistributionType
)


class Distribution(BaseModel):
    name: str = Field(None)
    distribution_type: DistributionType = Field(None)
    distribution_name: str = Field(None)
    distribution_filename: str = Field(None)
    distribution_extra_arguments: dict = Field(None)


class DiseaseDistribution(BaseModel):
    type: DiseaseDistributionType = Field(...)
    distribution: Distribution = Field(...)


class NaturalDistribution(BaseModel):
    type: NaturalDistributionType = Field(...)
    distribution: Distribution = Field(...)
