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

from src.models.general import RestrictionType, UnitTime
from .base import BaseDocument
from .configuration import Configuration


class CyclicRestriction(EmbeddedDocument):
    grace_time = DateTimeField()
    global_quarantine = IntField()
    global_quarantine_units = EnumField(UnitTime)
    restriction_mode = EnumField(RestrictionType)
    time_without_restrictions = IntField()
    time_without_restrictions_units = EnumField(UnitTime)


class Quarantine(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    has_cyclic_restrictions = BooleanField(required=True)
    has_tracing_restrictions = BooleanField(required=True)
    cyclic_restrictions = EmbeddedDocumentField(CyclicRestriction, null=True)
    tracing_restrictions = DictField(null=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)


class QuarantineGroup(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    name = StringField()
    quarantine = ReferenceField(Quarantine, required=True)
