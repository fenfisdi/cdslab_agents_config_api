from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    EnumField,
    IntField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import (
    UnitLength, 
    UnitTime,
    ConfigurationVariableName
)
from .base import BaseDocument
from .user import User


class Variables(EmbeddedDocument):
    name = EnumField(ConfigurationVariableName, required=True)
    configured = BooleanField(default=False)

class IntervalDate(EmbeddedDocument):
    start = DateTimeField()
    end = DateTimeField()


class Configuration(BaseDocument):
    identifier = UUIDField(binary=False, unique=True)
    name = StringField()
    population_number = IntField()
    interval_date = EmbeddedDocumentField(IntervalDate)
    iteration_time_units = EnumField(UnitTime)
    iteration_number = IntField()
    box_size = DictField()
    distance_units = EnumField(UnitLength)
    is_deleted = BooleanField(default=False)
    user = ReferenceField(User, dbref=True, required=True)
    variables = EmbeddedDocumentListField(Variables)
