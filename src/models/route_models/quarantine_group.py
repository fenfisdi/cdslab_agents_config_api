from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.models.general import RestrictionType, TracingType, UnitTime


class QuarantineGroup(BaseModel):
    name: str = Field(...)


class TracingRestriction(BaseModel):
    start_percentage: float = Field(...)
    stop_mode: TracingType = Field(...)
    quarantine_stop_percentage: float = Field(None)
    quarantine_stop_length: int = Field(None)
    quarantine_stop_length_units: UnitTime = Field(None)


class CyclicRestriction(BaseModel):
    grace_time: datetime = Field(...)
    global_quarantine: int = Field(...)
    global_quarantine_units: UnitTime = Field(...)
    restriction_mode: RestrictionType = Field(...)
    time_without_restrictions: int = Field(None)
    time_without_restrictions_units: UnitTime = Field(None)


class UpdateQuarantine(BaseModel):
    has_cyclic_restrictions: bool = Field(None)
    has_tracing_restrictions: bool = Field(None)
    cyclic_restrictions: CyclicRestriction = Field(None)
    tracing_restrictions: TracingRestriction = Field(None)


class NewQuarantine(UpdateQuarantine):
    quarantine_groups: List[QuarantineGroup] = Field(...)


class UpdateQuarantineGroup(BaseModel):
    name: str = Field(None)
    delay: int = Field(None)
    delay_units: UnitTime = Field(None)
    length: int = Field(None)
    length_units: UnitTime = Field(None)
    unrestricted_time: int = Field(None)
    unrestricted_time_units: UnitTime = Field(None)
