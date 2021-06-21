from datetime import datetime
from pydantic import BaseModel, Field


class NewCyclicQuarantineRestriction(BaseModel):
    enabled: bool = Field(...)
    grace_time: datetime = Field(...)
    global_quarantine_length: int = Field(...)
    global_quarantine_length_units: str = Field(...)
    unrestricted_time_mode: str = Field(...)
    unrestricted_time: int = Field(...)
    unrestricted_time_units: str = Field(...)
