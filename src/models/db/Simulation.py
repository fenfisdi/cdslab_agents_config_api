from mongoengine import(
    UUIDField,
    ReferenceField,
    DateField,
    EnumField
)

from .base import BaseDocument
from .configuration import Configuration
from src.models.general.simulation import SimulationStatus


class Simulation(BaseDocument):
    identifer = UUIDField(binary=False, unique=True, required=True)
    configuration = ReferenceField(Configuration, dbref=True)
    status = EnumField(SimulationStatus, required=True)
    executed_at = DateField(required=True)
