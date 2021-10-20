from mongoengine import DictField, EmbeddedDocument, EmbeddedDocumentField, ListField, ReferenceField, UUIDField

from . import Configuration
from .base import BaseDocument


class ExtraData(EmbeddedDocument):
    chains = DictField(default={})


class Population(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    allowed_configuration = ListField()
    allowed_variables = ListField()
    values = DictField()
    extra_data = EmbeddedDocumentField(ExtraData, null=False)
