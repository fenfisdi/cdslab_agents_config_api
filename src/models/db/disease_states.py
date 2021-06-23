from mongoengine import (
    BooleanField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    EnumField,
    FloatField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import DistributionDiseaseType
from .base import BaseDocument
from .configuration import Configuration
from .distribution import Distribution


class DiseaseDistribution(EmbeddedDocument):
    type = EnumField(DistributionDiseaseType, required=True)
    distribution = EmbeddedDocumentField(Distribution)


class DiseaseGroups(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    name = StringField()
    can_infected = BooleanField(required=True)
    is_infected = BooleanField(required=True)
    can_spread = BooleanField(required=True)
    spread_radius = FloatField()
    spread_probability = FloatField()
    distributions = EmbeddedDocumentListField(DiseaseDistribution)
