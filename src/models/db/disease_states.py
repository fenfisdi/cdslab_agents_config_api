from mongoengine import(
    UUIDField,
    ReferenceField,
    StringField,
    BooleanField,
    FloatField,
    ListField
)

from .distribution import Distribution
from .configuration import Configuration
from .base import BaseDocument


class DiseaseStates(BaseDocument):
    identifer = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    name = StringField()
    can_get_infected = BooleanField(default=True)
    is_infected = BooleanField(default=False)
    can_spread = BooleanField(default=False)
    spread_radius = FloatField(default=2.5)
    spread_probability = FloatField(default=0.1)
    distributions = ListField(ReferenceField(Distribution))
