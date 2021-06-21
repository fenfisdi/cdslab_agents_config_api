from mongoengine import (
    Document,
    StringField,
    BooleanField,
    UUIDField
)


class QuarantineRestriction(Document):
    identifier = UUIDField(
        binary=False,
        unique=True,
        required=True
    )
    name = StringField(required=True)
    type = StringField(required=True)
    value = BooleanField(required=True)
