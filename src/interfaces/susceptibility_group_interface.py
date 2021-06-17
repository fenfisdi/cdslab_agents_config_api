from src.models import (
    SusceptibilityGroup,
    Configuration
)


class SusceptibilityGroupInterface:
    """
    Interface to consult susceptibility groups in db
    """

    @staticmethod
    def find_all():
        """
        Find all existing mobility groups in db
        """
        return SusceptibilityGroup.objects().all()

    @staticmethod
    def find_one(identifier: str):
        """
        Find a existing mobility group in db
        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return SusceptibilityGroup.objects(
            **filters
        ).first()

    @staticmethod
    def find_by_configuration(
            configuration: Configuration
    ):
        filters = dict(
            configuration=configuration
        )
        return SusceptibilityGroup.objects(
            **filters
        ).all()
