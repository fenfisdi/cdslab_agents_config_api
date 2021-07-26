from enum import Enum


class Groups(Enum):
    MOBILITY: str = "mobility"
    SUSCEPTIBILITY: str = "susceptibility"
    VULNERABILITY: str = "vulnerability"
    DISEASE: str = "disease"
    QUARANTINE: str = "quarantine"


class EnabledGroups(Groups):
    AGE: str = "age"
