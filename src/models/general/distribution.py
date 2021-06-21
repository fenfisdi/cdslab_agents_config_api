from enum import Enum


class DistributionType(Enum):
    CONSTANT: str = 'constant'
    EMPIRICAL: str = 'empirical'
    NUMPY: str = 'numpy'
    WEIGHTS: str = 'weights'
