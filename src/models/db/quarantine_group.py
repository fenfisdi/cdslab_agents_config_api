from mongoengine import Document, UUIDField, \
    ReferenceField, StringField, FloatField

from configuration import Configuration


class QuarantineGroup(Document):
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
    name = StringField(required=True)
