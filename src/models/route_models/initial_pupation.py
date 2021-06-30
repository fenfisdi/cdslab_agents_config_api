from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.general import ConfigurationVariableName

class NewInitialPopulationSetup(BaseModel):
    nesting_variables_names: List[str] = Field(...)
    percentages: dict = Field(...)
    variable_name: ConfigurationVariableName = Field(...)
    