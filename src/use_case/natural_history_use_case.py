from uuid import UUID
from src.interfaces import VulnerabilityGroupInterface, \
    DiseaseStatesInterface,ConfigurationInterface

from src.utils import ConfigurationMessage, VulnerabilityGroupMessage, \
    DiseaseStatesMessage

class NaturalHistoryUseCase:

    @classmethod
    def validate_parameters(
        cls, 
        config: UUID,
        vulnerability_group: UUID,
        disease_state: UUID
    ):

        config_found = ConfigurationInterface.find_by_identifier(config)
        group_found = VulnerabilityGroupInterface.find_by_identifier(
            vulnerability_group
        )
        states_found = DiseaseStatesInterface.find_by_identifier(
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
