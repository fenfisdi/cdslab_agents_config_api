from uuid import UUID

from src.models.db import Configuration, MobilityGroup


class MobilityGroupInterface:
    """
    Interface to consult mobility groups in db
    """

    @staticmethod
    def find_all():
        """
        Find all existing mobility groups in db
        """
        return MobilityGroup.objects().all()

    @staticmethod
    def find_one(identifier: UUID) -> MobilityGroup:
        """
        Find a existing mobility group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return MobilityGroup.objects(**filters).first()

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        """
        Find all existing mobility groups by configuration in db

        :param configuration: Configuration object
        """
        filters = dict(
            configuration=configuration
        )
        return MobilityGroup.objects(**filters).all()
