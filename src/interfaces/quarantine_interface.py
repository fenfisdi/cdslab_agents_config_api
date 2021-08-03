from uuid import UUID

from src.models.db import Configuration, Quarantine, QuarantineGroup


class QuarantineInterface:

    @staticmethod
    def find_one_by_configuration(configuration: Configuration) -> Quarantine:
        filters = dict(
            configuration=configuration,
        )
        return Quarantine.objects(**filters).first()


class QuarantineGroupInterface:
    """
    Interface to consult quarantine groups in db
    """

    @staticmethod
    def find_one_by_identifier(identifier: UUID) -> QuarantineGroup:
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
    def find_one_by_configuration(
        configuration: Configuration
    ) -> QuarantineGroup:
        """
        Get all existing quarantine groups by
        configuration in db
        """
        filters = dict(
            configuration=configuration
        )
        return QuarantineGroup.objects(**filters).first()

    @staticmethod
    def find_all_by_conf(configuration: Configuration):
        filters = dict(
            configuration=configuration,
        )
        quarantine: Quarantine = Quarantine.objects(**filters).first()
        quarantine_filters = dict(
            quarantine=quarantine
        )

        return QuarantineGroup.objects(**quarantine_filters).all()
