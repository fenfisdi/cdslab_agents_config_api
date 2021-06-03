from mongoengine import (
    StringField,
    DictField,
    UUIDField,
    ListField
)

from .base import BaseDocument

class Distribution(BaseDocument):
    identifer = UUIDField(unique=True)
    name = StringField(required=True)
    type = ListField(required=True)
    selected = StringField()
    filename = StringField()
    extra_arguments = ListField()
