from uuid import UUID

from src.models.db import Configuration, DiseaseGroup
from src.models.db.master.disease_states import MasterDiseaseStates


class DiseaseStateInterface:
    """
    Interface to consult disease states in DB
    """

    @staticmethod
    def find_all():
        """
        Find all disease states
        """
        return MasterDiseaseStates.objects().all()

    @staticmethod
    def find_by_identifier(identifier: UUID) -> DiseaseGroup:
        """

        :param identifier: Identifier to search the configuration
        """

        filters = dict(
            identifier=identifier
        )
        return DiseaseGroup.objects(**filters).first()


class DiseaseGroupInterface:

    @staticmethod
    def find_all(configuration: Configuration):
        filters = dict(
            configuration=configuration,
        )
        return DiseaseGroup.objects(**filters).all()

    @staticmethod
    def find_one(identifier: UUID) -> DiseaseGroup:
        filters = dict(
            identifier=identifier
        )
        return DiseaseGroup.objects(**filters).first()
