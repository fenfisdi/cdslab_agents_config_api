from enum import Enum


class RestrictionType(Enum):
    FIXED: str = 'fixed'
    RANDOM: str = 'random'


class TracingType(Enum):
    PERCENTAGE: str = 'percentage'
    LENGTH: str = 'length'
