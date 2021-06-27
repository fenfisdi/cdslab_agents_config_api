from pydantic import BaseModel, Field

from src.models.general import (
    DiseaseDistributionType,
    DistributionType,
    NaturalDistributionType
)


class Distribution(BaseModel):
    name: str = Field(None)
    dist_type: DistributionType = Field(None)
    constant: float = Field(None)
    dist_name: str = Field(None)
    filename: str = Field(None)
    kwargs: dict = Field(None)


class DiseaseDistribution(BaseModel):
    type: DiseaseDistributionType = Field(...)
    distribution: Distribution = Field(...)


class NaturalDistribution(BaseModel):
    type: NaturalDistributionType = Field(...)
    distribution: Distribution = Field(...)
