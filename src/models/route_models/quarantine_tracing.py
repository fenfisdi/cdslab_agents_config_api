from pydantic import BaseModel, Field


class NewQuarantineTracing(BaseModel):
    variable_to_trace: str = Field(...)
    quarantine_start_percentage: float = Field(...)
    quarantine_stop_mode: str = Field(...)
    quarantine_stop_percentage: float = Field(...)
    quarantine_length: int = Field(...)
    quarantine_length_units: str = Field(...)
    target_groups: list = Field(...)
