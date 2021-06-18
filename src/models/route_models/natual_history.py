from uuid import UUID
from pydantic import BaseModel, Field

class NewNaturalHistory(BaseModel):
    identiffer: UUID = Field(...)
    