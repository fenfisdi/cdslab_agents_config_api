from uuid import UUID

from src.models.db import Configuration, NaturalHistory


class NaturalHistoryInterface:
    """
    Interface to consult natural history in DB
    """

    @staticmethod
    def find_one(identifier: UUID):
        """
        Get a natural history by identifier

        :param identifier: natural history id
        """

        filters = dict(
            identifier=identifier
        )

        return NaturalHistory.objects(**filters).first()

    @staticmethod
    def find_by_config(configuration: Configuration):
        filters = dict(
            configuration=configuration
        )
        return NaturalHistory.objects(**filters).all()
