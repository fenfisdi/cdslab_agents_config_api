from mongoengine import (
    BooleanField,
    DictField,
    EnumField,
    IntField,
    ReferenceField,
    StringField,
    UUIDField
)

from src.models.general import UnitLength, UnitTime
from .base import BaseDocument
from .user import User


class Configuration(BaseDocument):
    identifier = UUIDField(binary=False, unique=True)
    name = StringField()
    population_number = IntField()
    interval_date = DictField()
    iteration_time_units = EnumField(UnitTime)
    iteration_number = IntField()
    box_size = DictField()
    distance_units = EnumField(UnitLength)
    is_deleted = BooleanField(default=False)
    user = ReferenceField(User, dbref=True, required=True)
