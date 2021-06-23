from uuid import UUID
from typing import Union

from mongoengine import Document

from src.interfaces import (
    DiseaseStatesInterface,
    VulnerabilityGroupInterface,
    AgeGroupInterface,
    MobilityGroupInterface,
    NaturalHistoryInterface,
    ConfigurationInterface
)
from src.models.db import User
from src.utils import BsonObject


class InitialPopulationUseCase:

    @classmethod
    def find_parameters(
        cls, 
        config_id: UUID,
        user: User
    ):
        """
        find all configuration parameters 

        :param config_id: configuration id
        """

        config = ConfigurationInterface.find_by_identifier(config_id, user)

        natural_history = NaturalHistoryInterface.find_by_configuration(config)
        disease_state = DiseaseStatesInterface.find_by_configuration(config)
        vulnerability_group = VulnerabilityGroupInterface.find_by_configuration(
            config
        )
        age_group = AgeGroupInterface.find_by_configuration(config)
        mobility_group = MobilityGroupInterface.find_by_configuration(config)

        parameters_found = []

        if disease_state:
            parameters_found.append(
                cls.get_information(disease_state)
            )
        if vulnerability_group:
            parameters_found.append(
                cls.get_information(vulnerability_group)
            )
        if age_group:
            parameters_found.append(
                cls.get_information(age_group)
            )
        if mobility_group:
            parameters_found.append(
                cls.get_information(mobility_group)
            )
        if natural_history:
            parameters_found.append(
                cls.get_information(natural_history)
            )

        return parameters_found

    
    @classmethod
    def get_information(cls, parameter: Union[Document, Document]):
        """
        Gets the type and identifier of the parameter

        :param parameter: mongo document
        """
        data = BsonObject.dict(parameter,True)

        return dict(
            variable=data.get("_cls"),
            identifier=data.get("identifier")
        )