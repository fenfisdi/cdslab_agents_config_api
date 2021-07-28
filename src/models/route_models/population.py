from typing import Dict, Set, Union
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.general import Groups


class BasicStruct(BaseModel):
    uuid: UUID = Field(...)
    value: Union[dict, float] = Field(...)


class UpdateVariable(BaseModel):
    variable: Groups = Field(...)
    chain: Set[Groups] = Field(...)
    values: Dict[str, BasicStruct] = Field(None)

    class Config:
        use_enum_values = True
