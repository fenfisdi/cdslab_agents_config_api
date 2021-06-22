from mongoengine import (
    UUIDField,
    ReferenceField,
    StringField,
    FloatField
)

from .configuration import Configuration
from .base import BaseDocument


class AgeGroup(BaseDocument):
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
    name = StringField(required=True)
    population_percentage = FloatField(required=True)
