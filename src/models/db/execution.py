from mongoengine import (
    EnumField,
    IntField
)

from src.models.db.base import BaseDocument
from src.models.general import UserRole


class RoleMachine(BaseDocument):
    role = EnumField(UserRole, unique=True)
    max_machine = IntField(null=False, required=True)
    default_memory = IntField(default=2048, null=False, required=True)
    default_cpu = IntField(default=1, null=False, required=True)
