from enum import Enum


class DistributionType(Enum):
    CONSTANT: str = 'constant'
    EMPIRICAL: str = 'empirical'
    NUMPY: str = 'numpy'
    WEIGHTS: str = 'weights'


class DistributionDiseaseType(Enum):
    DIAGNOSIS: str = 'diagnosis'
    ISOLATION: str = 'isolation'
    HOSPITAL: str = 'hospitalization'
    ICU: str = 'icu'
