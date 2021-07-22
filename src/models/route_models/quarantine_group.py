from datetime import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.general import (
    RestrictionType,
    TracingType,
    TracingVariables,
    UnitTime
)


class QuarantineVariable(BaseModel):
    name: str = Field(None)
    delay: int = Field(None)
    delay_units: UnitTime = Field(None)
    length: int = Field(None)
    length_units: UnitTime = Field(None)
    unrestricted_time: int = Field(None)
    unrestricted_time_units: UnitTime = Field(None)


class TracingRestriction(BaseModel):
    start_percentage: float = Field(...)
    stop_mode: TracingType = Field(...)
    stop_percentage: float = Field(None)
    stop_length: int = Field(None)
    stop_length_units: UnitTime = Field(None)
    variables: Dict[UUID, bool] = Field(None)


class CyclicRestriction(BaseModel):
    grace_time: datetime = Field(...)
    global_quarantine: int = Field(...)
    global_quarantine_units: UnitTime = Field(...)
    restriction_mode: RestrictionType = Field(...)
    time_without_restrictions: int = Field(None)
    time_without_restrictions_units: UnitTime = Field(None)
    variables: Dict[UUID, QuarantineVariable] = Field(None)


Tracing = Dict[TracingVariables, TracingRestriction]


class UpdateQuarantine(BaseModel):
    has_cyclic_restrictions: bool = Field(None)
    has_tracing_restrictions: bool = Field(None)
    cyclic_restrictions: CyclicRestriction = Field(None)
    tracing_restrictions: Tracing = Field(None)


class QuarantineGroup(BaseModel):
    name: str = Field(...)


class NewQuarantine(UpdateQuarantine):
    quarantine_groups: List[QuarantineGroup] = Field(...)
