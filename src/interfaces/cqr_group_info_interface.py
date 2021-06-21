from uuid import UUID

from src.models import (
    Configuration,
    CQRGroupInfo
)


class CQRGroupInfoInterface:
    """
    Interface to consult CQRGroupInfo in db
    """

    @staticmethod
    def find_one(identifier: UUID) -> CQRGroupInfo:
        """
        Find a CQRGroupInfo in db

        :param identifier: CQRGroupInfo identifier
        """
        filters = dict(
            identifier=identifier
        )
        return CQRGroupInfo.objects(**filters).firts()

    @staticmethod
    def find_by_configuration(
            configuration: Configuration
    ):
        """
        Find all CQRGroupInfo by configuration and quarantine group in db

        :param configuration: Configuration to search
        """
        filters = dict(
            configuration=configuration
        )
        return CQRGroupInfo.objects(**filters).all()
