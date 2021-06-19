from enum import Enum


class DiseaseState(Enum):
    DIAGNOSIS: str = 'diagnosis'
    QUARANTINE: str = 'quarantine'
    HOSPITAL: str = 'hospitalization'
    UCI: str = 'uci'
