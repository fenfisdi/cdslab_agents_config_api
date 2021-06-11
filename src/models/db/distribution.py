from mongoengine import UUIDField, StringField, DictField

from .base import BaseDocument

class Distribution(BaseDocument):
    identifier = UUIDField(
        binary=False,
        unique=True,
        required=True
    )
    name = StringField(required=True)
    distribution_type = StringField(required=True)
    distribution_name = StringField()
    distribution_filename = StringField()
    distribution_extra_arguments = DictField()
    