from mongoengine import DictField, ListField, ReferenceField, UUIDField

from . import Configuration
from .base import BaseDocument


class Population(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    allowed_configuration = ListField()
    allowed_variables = ListField()
    values = DictField()
