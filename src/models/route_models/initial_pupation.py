from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class NewInitialPopulationSetup(BaseModel):
    nesting_variables_names: List[str] = Field(...)
    nesting_varibles_id: List[str] = Field(...)
    percentages: dict = Field(
        {
            "Group 1" : {
                "Group 2": {
                    "Percentage": "value"
                }
            }
        }
    )
    
class UpdateInitialPopulationSetup(NewInitialPopulationSetup):
    identifier: UUID = Field(...)
