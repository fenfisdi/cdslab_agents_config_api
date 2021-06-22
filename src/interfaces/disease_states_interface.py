from uuid import UUID

from src.models.db.master.disease_states import MasterDiseaseStates
from src.models.db.disease_states import DiseaseStates
from src.models.db import Configuration


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
    def find_by_identifier(identifier: UUID):
        """
        Get disease states by identifier

        :param identifier: Identifier to search the configuration
        """

        filters = dict(
            identifier=identifier
        )
        return DiseaseStates.objects(**filters).first()

    @staticmethod
    def find_by_configuration(configuration: Configuration):
        """
        Get disease states by configuration

        :param configuration: configuration information
        """
        filters = dict(
            configuration=configuration
        )
        return DiseaseStates.objects(**filters).first()
