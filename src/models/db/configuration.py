from mongoengine import StringField, UUIDField, \
    IntField, BooleanField, DictField

from .base import BaseDocument


class Configuration(BaseDocument):
    identifier = UUIDField(binary=False, unique=True)
    name = StringField()
    population_number = IntField()
    interval_date = DictField()
    iteration_time_units = StringField()
    iteration_number = IntField()
    box_size = DictField()
    distance_units = StringField()
    is_delete = BooleanField(default=False)
