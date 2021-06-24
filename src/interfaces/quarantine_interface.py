from uuid import UUID

from src.models.db import Configuration, Quarantine, QuarantineGroup


class QuarantineInterface:

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        filters = dict(
            configuration=configuration,
        )
        return Quarantine.objects(**filters).first()


class QuarantineGroupInterface:
    """
    Interface to consult quarantine groups in db
    """

    @staticmethod
    def find_by_identifier(identifier: UUID) -> QuarantineGroup:
        """
        Get a existing quarantine group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return QuarantineGroup.objects(**filters).first()

    @staticmethod
    def find_all(quarantine: Quarantine):
        """
        Get all existing quarantine groups in db
        """
        filters = dict(
            quarantine=quarantine
        )
        return QuarantineGroup.objects(**filters).all()

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
        return QuarantineGroup.objects(**filters).one()
