from mongoengine import UUIDField, \
    ReferenceField, StringField

from .base import BaseDocument
from configuration import Configuration
from distribution import Distribution


class SusceptibilityGroup(BaseDocument):
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
    distribution = ReferenceField(
        Distribution,
        dbref=True,
        required=True
    )
    name = StringField(required=True)
