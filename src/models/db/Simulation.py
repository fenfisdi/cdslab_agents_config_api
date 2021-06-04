from mongoengine import(
    StringField,
    UUIDField,
    IntField,
    DictField,
    ListField,
    DateTimeField,
    ReferenceField,
    DateField
)
from mongoengine.fields import BooleanField


from .base import BaseDocument

class Configuration(BaseDocument):
    identifer = UUIDField(unique=True)
    name = StringField()
    population_number = IntField()
    interval_date = ListField()
    iteration_time_units = StringField()
    iteration_number = IntField()
    box_size = ListField()
    distance_units = StringField()
    is_delete = BooleanField(default=False)

class Simulation(BaseDocument):
    identifer = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    executed_at = DateField(required=True)
