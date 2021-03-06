from pydantic import BaseModel, Field

from src.models.general import (
    DiseaseDistributionType,
    DistributionType,
    NaturalDistributionType
)


class Distribution(BaseModel):
    type: DistributionType = Field(...)
    numpy_type: str = Field(None)
    kwargs: dict = Field(None)

    class Config:
        use_enum_values = True


class DiseaseDistribution(BaseModel):
    type: DiseaseDistributionType = Field(...)
    distribution: Distribution = Field(...)


class NaturalDistribution(BaseModel):
    type: NaturalDistributionType = Field(...)
    distribution: Distribution = Field(...)
