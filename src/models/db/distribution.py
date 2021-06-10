from mongoengine import UUIDField, StringField, \
    DictField

from .base import BaseDocument


class Distribution(BaseDocument):
    identifier = UUIDField(binary=False, unique=True, required=True)
    name = StringField(required=True)
    distribution_type = StringField(required=True)
    filename = StringField(required=True)
    extra_arguments = DictField(required=True)
