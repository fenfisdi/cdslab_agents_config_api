from typing import Dict, Set

from pydantic import BaseModel, Field

from src.models.general import Groups


class UpdateVariable(BaseModel):
    variable: Groups = Field(...)
    chain: Set[Groups] = Field(...)
    values: Dict[str, dict] = Field(None)

    class Config:
        use_enum_values = True
