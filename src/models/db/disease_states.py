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

from src.models.general import DiseaseDistributionType, UnitLength
from .base import BaseDocument
from .configuration import Configuration
from .distribution import Distribution


class DiseaseDistribution(EmbeddedDocument):
    type = EnumField(DiseaseDistributionType, required=True)
    distribution = EmbeddedDocumentField(Distribution)


class DiseaseGroup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    name = StringField()
    is_death = BooleanField(default=False)
    can_infected = BooleanField(required=True)
    is_infected = BooleanField(required=True)
    can_spread = BooleanField(required=True)
    spread_radius = FloatField()
    spread_radius_unit = EnumField(UnitLength)
    spread_probability = FloatField()
    distributions = EmbeddedDocumentListField(DiseaseDistribution)
