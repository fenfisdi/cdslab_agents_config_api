from mongoengine import (
    UUIDField,
    ReferenceField,
    EmbeddedDocumentListField,
    FloatField,
    DictField
)

from .base import BaseDocument
from .configuration import Configuration
from .disease_states import DiseaseStates
from .distribution import Distribution
from .vulnerability_group import VulnerabilityGroup


class NaturalHistory(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    vulnerability_group = ReferenceField(VulnerabilityGroup, dbref=True)
    disease_state = ReferenceField(DiseaseStates, dbref=True)
    distribution = EmbeddedDocumentListField(Distribution)
    avoidance_radius = FloatField()
    transitions = DictField()
