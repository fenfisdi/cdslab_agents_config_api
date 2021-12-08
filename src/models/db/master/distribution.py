from mongoengine import (
    Document,
    StringField,
    ListField
)


class MasterDistribution(Document):
    name = StringField(required=True)
    type = ListField(required=True)
    