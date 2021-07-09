from uuid import uuid1

from src.interfaces import DiseaseGroupInterface
from src.models.db import Configuration, DiseaseGroup


class VerifyDefaultState:

    @classmethod
    def handle(cls, configuration: Configuration) -> None:
        states = DiseaseGroupInterface.find_all(configuration)

        death_state = next((state for state in states if state.is_death), None)
        if not death_state:
            DiseaseGroup(
                identifier=uuid1(),
                configuration=configuration,
                name="death",
                is_death=True,
                can_infected=False,
                is_infected=False,
                can_spread=False
            ).save()
