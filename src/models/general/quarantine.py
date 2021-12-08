from enum import Enum


class RestrictionType(Enum):
    FIXED: str = 'fixed'
    RANDOM: str = 'random'


class TracingType(Enum):
    PERCENTAGE: str = 'percentage'
    LENGTH: str = 'length'


class TracingVariables(Enum):
    DEAD_BY_DISEASE: str = 'dead by disease'
    DIAGNOSED: str = 'meters'
    ICU: str = 'ICU capacity'
    HOSPITAL_CAPACITY: str = 'hospital capacity'
