from pydantic import BaseModel, Field


class NewQuarantineGroup(BaseModel):
    identifier: str = Field(...)
    configuration: str = Field(...)
    name: str = Field(...)
