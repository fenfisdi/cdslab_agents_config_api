from uuid import UUID

from src.models.db import (
    Configuration,
    DiseaseGroup,
    NaturalHistory,
    VulnerabilityGroup
)


class NaturalHistoryInterface:
    """
    Interface to consult natural history in DB
    """

    @staticmethod
    def find_one(
        vulnerability_group: VulnerabilityGroup,
        disease_state: DiseaseGroup
    ) -> NaturalHistory:
        filters = dict(
            vulnerability_group=vulnerability_group,
            disease_group=disease_state
        )
        return NaturalHistory.objects(**filters).first()

    @staticmethod
    def find_one_by_id(
        identifier: UUID,
        configuration: Configuration
    ) -> NaturalHistory:
        """
        Get a natural history by identifier

        :param identifier: natural history id.
        :param configuration: Natural history configuration:
        """

        filters = dict(
            identifier=identifier,
            configuration=configuration
        )

        return NaturalHistory.objects(**filters).first()

    @staticmethod
    def find_all_by_config(configuration: Configuration):
        filters = dict(
            configuration=configuration
        )
        return NaturalHistory.objects(**filters).all()
