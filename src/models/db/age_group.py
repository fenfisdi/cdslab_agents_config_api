from mongoengine import Document, UUIDField, ReferenceField, StringField, FloatField

from configuration import Configuration


class AgeGroup(Document):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    name = StringField()
    population_percentage = FloatField()

