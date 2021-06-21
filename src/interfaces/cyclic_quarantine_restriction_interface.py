from uuid import UUID

from src.models import (
    Configuration,
    CyclicQuarantineRestriction
)


class CyclicQuarantineRestrictionsInterface:
    """
    Interface to consult CyclicQuarantineRestrictions in db
    """

    @staticmethod
    def find_by_identifier(identifier: UUID):
        """
        Find a CyclicQuarantineRestrictions in db

        :param identifier: CyclicQuarantineRestrictions identifier
        """
        filters = dict(
            identifier=identifier
        )
        return CyclicQuarantineRestriction.objects(**filters).first()

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        """
        Find a CyclicQuarantineRestrictions by configuration in db

        :param configuration: Configuration to search
        """
        filters = dict(
            configuration=configuration
        )
        return CyclicQuarantineRestriction.objects(**filters).first()
