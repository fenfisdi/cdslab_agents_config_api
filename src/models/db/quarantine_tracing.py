from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EnumField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import RestrictionType, TracingType, UnitTime
from .base import BaseDocument
from .configuration import Configuration


class CyclicRestriction(EmbeddedDocument):
    grace_time = DateTimeField()
    global_quarantine = IntField()
    global_quarantine_units = EnumField(UnitTime)
    restriction_mode = EnumField(RestrictionType)
    time_without_restrictions = IntField()
    time_without_restrictions_units = EnumField(UnitTime)


class TracingRestriction(EmbeddedDocument):
    start_percentage = FloatField(required=True)
    stop_mode = EnumField(TracingType, required=True)
    quarantine_stop_percentage = FloatField()
    quarantine_stop_length = IntField()
    quarantine_stop_length_units = EnumField(UnitTime)


class Quarantine(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    has_cyclic_restrictions = BooleanField(required=True)
    has_tracing_restrictions = BooleanField(required=True)
    cyclic_restrictions = EmbeddedDocumentField(CyclicRestriction, null=True)
    tracing_restrictions = EmbeddedDocumentField(TracingRestriction, null=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)


class QuarantineGroup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    name = StringField()
    delay = IntField()
    delay_units = EnumField(UnitTime)
    length = IntField()
    length_units = EnumField(UnitTime)
    unrestricted_time = IntField()
    unrestricted_time_units = EnumField(UnitTime)
    quarantine = ReferenceField(Quarantine, required=True)


class QuarantineTracing(Document):
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
    variable_to_trace = StringField(required=True)
    quarantine_start_percentage = FloatField(required=True)
    quarantine_stop_mode = StringField(required=True)
    quarantine_stop_percentage = FloatField()
    quarantine_length = IntField()
    quarantine_length_units = StringField()
    target_groups = ListField(QuarantineGroup)
