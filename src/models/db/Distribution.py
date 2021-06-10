from mongoengine import(
    UUIDField,
    StringField,
    DictField
)

from .base import BaseDocument


class Distribution(BaseDocument):
    identifer = UUIDField(binary=False, unique=True, required=True)
    name = StringField(required=True)
    distribution_type = StringField()
    filename = StringField()
    extra_arguments = DictField()
    