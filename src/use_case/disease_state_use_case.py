from typing import Union
from uuid import UUID, uuid1

from src.interfaces import DiseaseGroupInterface
from src.models.db import Configuration, DiseaseGroup
from src.models.general import DiseaseDistributionType


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


class VerifyDiseaseStateDistribution:

    @classmethod
    def handle(
        cls,
        disease_group: DiseaseGroup,
        distribution: DiseaseDistributionType
    ):
        distributions: dict = disease_group.distributions
        if distributions and distributions.get(distribution.value):
            return True
        return False


class SaveDiseaseDistributionFile:

    @classmethod
    def handle(
        cls,
        disease_group: DiseaseGroup,
        distribution: DiseaseDistributionType,
        file_id: Union[UUID, str]
    ):
        distributions = disease_group.distributions
        new_distributions = dict()
        for k, v in distributions.items():
            if k == distribution.value:
                v.update({"file_id": file_id})

            new_distributions.update({k: v})

        disease_group.distributions.update(new_distributions)
        disease_group.save().reload()


class UpdateDistributionsInfo:

    @classmethod
    def handle(cls, base_distribution: dict, distribution: dict) -> dict:
        updated_distributions = dict()
        for k, v in base_distribution.items():
            temp_distribution = distribution.get(k)
            if temp_distribution:
                v.update(temp_distribution)
            updated_distributions[k] = v

        for k, v in distribution.items():
            if k not in updated_distributions:
                updated_distributions[k] = v

        return updated_distributions
