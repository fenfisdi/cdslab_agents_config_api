from pydantic import BaseModel, Field


class NewCQRGroupInfo(BaseModel):
    quarantine_identifier: str = Field(...)
    delay: int = Field(...)
    delay_units: str = Field(...)
    quarantine_length: int = Field(...)
    quarantine_length_units: str = Field(...)
    unrestricted_time: int = Field(...)
    unrestricted_time_units: str = Field(...)
