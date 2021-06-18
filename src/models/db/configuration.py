from mongoengine import (
    BooleanField,
    DictField,
    IntField,
    ReferenceField,
    StringField,
    UUIDField
)

from .base import BaseDocument
from .user import User


class Configuration(BaseDocument):
    identifier = UUIDField(binary=False, unique=True)
    name = StringField()
    population_number = IntField()
    interval_date = DictField()
    iteration_time_units = StringField()
    iteration_number = IntField()
    box_size = DictField()
    distance_units = StringField()
    is_deleted = BooleanField(default=False)
    user = ReferenceField(User, dbref=True, required=True)
