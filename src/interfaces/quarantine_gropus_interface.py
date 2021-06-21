from uuid import UUID

from src.models import (
    QuarantineGroup,
    Configuration
)


class QuarantineGroupInterface:
    """
    Interface to consult quarantine groups in db
    """

    @staticmethod
    def find_by_identifier(identifier: UUID):
        """
        Get a existing quarantine group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return QuarantineGroup.objects(**filters).first()

    @staticmethod
    def find_all():
        """
        Get all existing quarantine groups in db
        """
        return QuarantineGroup.objects().all()

    @staticmethod
    def find_by_configuration(
            configuration: Configuration
    ):
        """
        Get all existing quarantine groups by
        configuration in db
        """
        filters = dict(
            configuration=configuration
        )
        return QuarantineGroup.objects(**filters).all()
