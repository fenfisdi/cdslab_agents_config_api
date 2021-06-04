from mongoengine import (
    Document,
    StringField,
    ListField
)

class Distribution(Document):
    name = StringField(required=True)
    type = ListField(required=True)
    