from uuid import UUID

from src.models.db import AgeGroup, Configuration


class AgeGroupInterface:
    """
    Interface to consult age groups in DB
    """

    @staticmethod
    def find_one(identifier: UUID) -> AgeGroup:
        """
        Get a existing age group by identifier in db
        """
        filters = dict(
            identifier=identifier
        )
        return AgeGroup.objects(**filters).first()

    @staticmethod
    def find_all_by_conf(configuration: Configuration):
        """
        Get all existing age groups in db relation to a configuration.

        :param configuration: Identifier from a configuration.
        """
        filters = dict(
            configuration=configuration
        )
        return AgeGroup.objects(**filters).all()
