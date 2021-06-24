from uuid import UUID

from src.models.db import Configuration, DiseaseGroups
from src.models.db.master.disease_states import MasterDiseaseStates


class DiseaseStatesInterface:
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
    def find_by_identifier(identifier: UUID) -> DiseaseGroups:
        """

        :param identifier: Identifier to search the configuration
        """

        filters = dict(
            identifier=identifier
        )
        return DiseaseGroups.objects(**filters).first()


class DiseaseGroupsInterface:

    @staticmethod
    def find_all(configuration: Configuration):
        filters = dict(
            configuration=configuration,
        )
        return DiseaseGroups.objects(**filters).all()

    @staticmethod
    def find_one(identifier: UUID) -> DiseaseGroups:
        filters = dict(
            identifier=identifier
        )
        return DiseaseGroups.objects(**filters).first()
