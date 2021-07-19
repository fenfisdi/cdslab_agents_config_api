from typing import Union
from uuid import UUID

from src.interfaces import (
    ConfigurationInterface,
    DiseaseStateInterface,
    VulnerabilityGroupInterface
)
from src.models.db import NaturalHistory
from src.models.general import NaturalDistributionType
from src.utils import (
    ConfigurationMessage,
    DiseaseStatesMessage,
    VulnerabilityGroupMessage
)


class NaturalHistoryUseCase:

    @classmethod
    def validate_parameters(
        cls,
        config: UUID,
        vulnerability_group: UUID,
        disease_state: UUID
    ):
        config_found = ConfigurationInterface.find_one_by_id(config)
        group_found = VulnerabilityGroupInterface.find_one_by_id(
            vulnerability_group
        )
        states_found = DiseaseStateInterface.find_by_identifier(
            disease_state
        )

        if not config_found:
            return ConfigurationMessage.not_found
        elif not group_found:
            return VulnerabilityGroupMessage.not_found
        elif not states_found:
            return DiseaseStatesMessage.not_found
        else:
            return dict(
                config=config_found,
                vulnerability_group=group_found,
                disease_states=states_found
            )


class VerifyNaturalHistoryDistribution:

    @classmethod
    def handle(
        cls,
        natural_history: NaturalHistory,
        distribution: NaturalDistributionType
    ) -> bool:
        distributions: dict = natural_history.distributions
        if distributions and distributions.get(distribution.value):
            return True
        return False


class SaveNaturalHistoryDistributionFile:

    @classmethod
    def handle(
        cls,
        natural_history: NaturalHistory,
        distribution: NaturalDistributionType,
        file_id: Union[UUID, str]
    ):
        distributions = natural_history.distributions
        new_distributions = dict()
        for k, v in distributions.items():
            if k == distribution.value:
                v.update({"file_id": file_id})

            new_distributions.update({k: v})

        natural_history.distributions.update(new_distributions)
        natural_history.save().reload()
