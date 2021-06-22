from mongoengine import (
    Document,
    UUIDField,
    ReferenceField,
    StringField,
    IntField,
    FloatField,
    ListField
)

from .configuration import Configuration
from .quarantine_group import QuarantineGroup


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
