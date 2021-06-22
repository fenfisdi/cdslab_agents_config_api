from mongoengine import UUIDField, ReferenceField, \
    StringField, BooleanField, FloatField, \
    EmbeddedDocumentListField


from .distribution import Distribution
from .configuration import Configuration
from .base import BaseDocument


class DiseaseStates(BaseDocument):
    identifier = UUIDField(
        binary=False,
        unique=True,
        required=True
    )
    configuration = ReferenceField(
        Configuration,
        dbref=True,
        required=True
    )
    name = StringField()
    can_get_infected = BooleanField(required=True)
    is_infected = BooleanField(required=True)
    can_spread = BooleanField(required=True)
    spread_radius = FloatField(required=True)
    spread_probability = FloatField(required=True)
    distributions = EmbeddedDocumentListField(Distribution)
