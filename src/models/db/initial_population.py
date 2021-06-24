from mongoengine import(
    UUIDField,
    ReferenceField,
    ListField,
    DictField
)

from .base import BaseDocument
from .configuration import Configuration


class InitialPopulationSetup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    nesting_variables_names = ListField()
    percentages = DictField()
    