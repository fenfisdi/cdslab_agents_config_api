from mongoengine import StringField

from .base import BaseDocument


class User(BaseDocument):
    name = StringField()
    role = StringField(null=True, required=True)
    email = StringField(unique=True, required=True)
