from uuid import UUID

from src.models import NaturalHistory

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
