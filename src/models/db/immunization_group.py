from mongoengine import (
    EmbeddedDocumentField,
    ReferenceField,
    StringField,
    UUIDField
)

from .base import BaseDocument
from .configuration import Configuration
from .distribution import Distribution


class ImmunizationGroup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    name = StringField(required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    distribution = EmbeddedDocumentField(Distribution, required=True)
