from mongoengine import (
    BooleanField,
    DictField,
    EmbeddedDocument,
    EmbeddedDocumentField,
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
    name = StringField(required=True)
    is_death = BooleanField(default=False)
    can_infected = BooleanField()
    is_infected = BooleanField()
    can_spread = BooleanField()
    spread_radius = FloatField()
    spread_radius_unit = EnumField(UnitLength)
    spread_probability = FloatField()
    distributions = DictField(required=False)
