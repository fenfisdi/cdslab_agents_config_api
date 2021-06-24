from enum import Enum


class QuarantineTracingVariables(Enum):
    dead_by_disease: str = 'dead by disease'
    diagnosed: str = 'meters'
    ICU_capacity: str = 'ICU capacity'
    hospital_capacity: str = 'hospital capacity'
