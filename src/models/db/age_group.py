from mongoengine import (
    Document,
    UUIDField,
    ReferenceField,
    StringField,
    FloatField
)

from .configuration import Configuration


class AgeGroup(Document):
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
