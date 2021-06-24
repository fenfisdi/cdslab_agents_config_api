from uuid import UUID

from src.models.db import Configuration, ImmunizationGroup


class ImmunizationGroupInterface:
    """
    Interface to consult immunization groups in db.
    """

    @staticmethod
    def find_all():
        """
        Find all existing mobility groups in db.
        """
        return ImmunizationGroup.objects().all()

    @staticmethod
    def find_one(identifier: UUID):
        """
        Find a existing immunization group in db.

        :param identifier: Identifier to search.
        """
        filters = dict(
            identifier=identifier
        )
        return ImmunizationGroup.objects(**filters).first()

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        """
        Find all existing immunization groups by configuration in db.

        :param configuration: Configuration to search
        """
        filters = dict(
            configuration=configuration
        )
        return ImmunizationGroup.objects(**filters).all()
