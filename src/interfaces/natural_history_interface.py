from uuid import UUID

from src.models import NaturalHistory
from src.models.db import Configuration


class NaturalHistoryInterface:
    """
    Interface to consult natural history in DB
    """

    @staticmethod
    def find_by_identifier(identifier: UUID):
        """
        Get a natural history by identifier

        :param identifier: natural history id
        """

        filters = dict(
            identifier=identifier
        )

        return NaturalHistory.objects(**filters).first()

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        """
        Get disease states by configuration

        :param configuration: configuration information
        """
        filters = dict(
            configuration=configuration
        )
        return NaturalHistory.objects(**filters).first()
        