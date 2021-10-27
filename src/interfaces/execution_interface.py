from typing import Optional

from src.models.db import RoleMachine
from src.models.general import UserRole


class RoleMachineInterface:

    @classmethod
    def find_role_machine(cls, role: UserRole) -> Optional[RoleMachine]:
        filters = dict(
            role=role,
        )
        return RoleMachine.objects(**filters).first()
