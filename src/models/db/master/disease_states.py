from mongoengine import (
    Document,
    StringField,
    UUIDField
)


class MasterDiseaseStates(Document):
    identifier = UUIDField(binary=False, unique=True, required=True)
    name = StringField(required=True)
