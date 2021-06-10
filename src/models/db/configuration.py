from mongoengine import (
    StringField,
    UUIDField,
    IntField,
    ListField,
    BooleanField
)

from .base import BaseDocument


class Configuration(BaseDocument):
    identifer = UUIDField(binary=False, unique=True, required=True)
    name = StringField()
    population_number = IntField()
    interval_date = ListField()
    iteration_time_units = StringField()
    iteration_number = IntField()
    box_size = ListField()
    distance_units = StringField()
    is_delete = BooleanField(default=False)
