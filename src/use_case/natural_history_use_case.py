from uuid import UUID

from src.interfaces import (
    ConfigurationInterface,
    DiseaseStateInterface,
    VulnerabilityGroupInterface
)
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
