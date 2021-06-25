from enum import Enum

class ConfigurationVariableName(Enum):
    mobility: str = "Mobility Groups"
    disease: str = "Disease States"
    vulnerability: str = "Vulnerability Groups"
    quaratine: str = "Quarantine Groups"
    Age: str = "Age Groups"