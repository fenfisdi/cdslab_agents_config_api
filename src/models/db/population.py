from mongoengine import ReferenceField, UUIDField

from . import Configuration
from .base import BaseDocument


class Population(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
