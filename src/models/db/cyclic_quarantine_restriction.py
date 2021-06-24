from mongoengine import (
    Document,
    UUIDField,
    ReferenceField,
    StringField,
    IntField,
    BooleanField,
    DateTimeField
)

from .configuration import Configuration


class CyclicQuarantineRestriction(Document):
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
    enabled = BooleanField(required=True)
    grace_time = DateTimeField(required=True)
    global_quarantine_length = IntField(required=True)
    global_quarantine_length_units = StringField(required=True)
    unrestricted_time_mode = StringField(required=True)
    unrestricted_time = IntField()
    unrestricted_time_units = StringField()
