from mongoengine import (
    EmbeddedDocumentField,
    ReferenceField,
    StringField,
    UUIDField
)

from .base import BaseDocument
from .configuration import Configuration
from .distribution import Distribution


class MobilityGroup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    distribution = EmbeddedDocumentField(Distribution, required=True)
    name = StringField(required=True)
