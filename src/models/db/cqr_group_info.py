from mongoengine import (
    Document,
    UUIDField,
    ReferenceField,
    StringField,
    IntField
)

from .configuration import Configuration
from.quarantine_group import QuarantineGroup


class CQRGroupInfo(Document):
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
    quarantine_group = ReferenceField(
        QuarantineGroup,
        dbref=True,
        required=True
    )
    delay = IntField(required=True)
    delay_units = StringField(required=True)
    quarantine_length = IntField(required=True)
    quarantine_length_units = StringField(required=True)
    unrestricted_time = IntField(required=True)
    unrestricted_time_units = StringField(required=True)
