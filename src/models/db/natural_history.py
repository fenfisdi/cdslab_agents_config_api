from mongoengine import (
    UUIDField,
    ReferenceField,
    ListField,
    FloatField,
    DictField
)

from .base import BaseDocument
from .vulnerability_group import VulnerabilityGroup
from .disease_states import DiseaseStates
from .configuration import Configuration
from .distribution import Distribution

class NaturalHistory(BaseDocument):
    identifier = UUIDField(
        binary=False,
        unique=True,
        required=True
    )
    configuration = ReferenceField(Configuration, dbref=True)
    vulnerability_group = ReferenceField(VulnerabilityGroup, dbref=True)
    disease_state = ReferenceField(DiseaseStates, dbref=True)
    distribution = ListField(ReferenceField(Distribution)) #Se repite en disease_state
    avoidance_radius = FloatField()
    transitions = DictField()
