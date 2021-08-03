from uuid import UUID

from src.models.db import Configuration, SusceptibilityGroup


class SusceptibilityGroupInterface:
    """
    Interface to consult susceptibility groups in db
    """

    @staticmethod
    def find_all():
        """
        Find all existing susceptibility groups in db
        """
        return SusceptibilityGroup.objects().all()

    @staticmethod
    def find_one(identifier: UUID) -> SusceptibilityGroup:
        """
        Find a existing susceptibility group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier,
        )
        return SusceptibilityGroup.objects(**filters).first()

    @staticmethod
    def find_all_by_conf(configuration: Configuration) -> SusceptibilityGroup:
        filters = dict(
            configuration=configuration,
        )
        return SusceptibilityGroup.objects(**filters).all()
