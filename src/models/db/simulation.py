from mongoengine import (
    DateTimeField,
    Document,
    EnumField,
    ReferenceField,
    UUIDField
)

from src.models.general.simulation import SimulationStatus
from .configuration import Configuration


class Simulation(Document):
    identifier = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True, required=True)
    status = EnumField(SimulationStatus, required=True)
    executed_at = DateTimeField()
