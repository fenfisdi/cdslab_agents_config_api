from pydantic import BaseModel, Field

from src.models.general import DistributionDiseaseType, DistributionType


class Distribution(BaseModel):
    name: str = Field(None)
    distribution_type: DistributionType = Field(None)
    distribution_name: str = Field(None)
    distribution_filename: str = Field(None)
    distribution_extra_arguments: dict = Field(None)


class DiseaseDistribution(BaseModel):
    type: DistributionDiseaseType = Field(...)
    distribution: Distribution = Field(...)
