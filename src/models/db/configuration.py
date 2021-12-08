from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EnumField,
    IntField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import ExecutionStatus, UnitLength, UnitTime
from .base import BaseDocument
from .user import User


class Execution(EmbeddedDocument):
    status = EnumField(ExecutionStatus, null=False, required=True)
    start_date = DateTimeField(null=True)
    finish_date = DateTimeField(null=True)


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
    hospital_capacity = IntField()
    icu_capacity = IntField()
    execution = EmbeddedDocumentField(Execution, required=False, null=True)
    user = ReferenceField(User, dbref=True, required=True)
