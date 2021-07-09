from mongoengine import (
    DictField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    EnumField,
    FloatField,
    ReferenceField,
    UUIDField
)

from src.models.general import NaturalDistributionType, UnitLength
from .base import BaseDocument
from .configuration import Configuration
from .disease_states import DiseaseGroup
from .distribution import Distribution
from .vulnerability_group import VulnerabilityGroup


class NaturalDistribution(EmbeddedDocument):
    type = EnumField(NaturalDistributionType, required=True)
    distribution = EmbeddedDocumentField(Distribution)


class NaturalHistory(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    vulnerability_group = ReferenceField(VulnerabilityGroup, dbref=True)
    disease_group = ReferenceField(DiseaseGroup, dbref=True)
    distribution = EmbeddedDocumentListField(NaturalDistribution)
    avoidance_radius = FloatField()
    avoidance_radius_unit = EnumField(UnitLength)
    transitions = DictField()
