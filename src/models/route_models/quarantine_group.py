from pydantic import BaseModel, Field


class NewQuarantineGroup(BaseModel):
    name: str = Field(...)
