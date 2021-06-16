from uuid import UUID

from src.models import AgeGroup, Configuration


class AgeGroupInterface:
    """
    Interface to consult age groups in DB
    """

    @staticmethod
    def find_one(identifier: str):
        """
        Get a existing age group by identifier in db
        """
        filters = dict(
            identifier=identifier
        )
        return AgeGroup.objects(**filters).first()

    @staticmethod
    def find_all():
        """
        Get all existing age groups in db
        """
        return AgeGroup.objects().all()

    @staticmethod
    def find_by_configuration(configuration_identifier: Configuration):
        """
        Get all existing age groups in db relation to a configuration

        :param configuration_identifier: Identifier from a configuration
        """
        filters = dict(
            configuration=configuration_identifier
        )
        return AgeGroup.objects(**filters).all()
