from uuid import UUID
from typing import Union

from mongoengine import Document

from src.interfaces import (
    ConfigurationInterface,
    DiseaseGroupsInterface,
    ImmunizationGroupInterface,
    MobilityGroupInterface,
    SusceptibilityGroupInterface,
    VulnerabilityGroupInterface
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

        disease_state = DiseaseGroupsInterface.find_all(config)
        vulnerability_group = VulnerabilityGroupInterface.find_by_configuration(
            config
        )
        
        mobility_group = MobilityGroupInterface.find_by_configuration(config)
        immunization_group = ImmunizationGroupInterface.find_by_configuration(config)
        susceptibility_group = SusceptibilityGroupInterface.find_by_conf(config)

        parameters_found = []

        if disease_state:
            parameters_found.append(
                cls.get_information(disease_state)
            )

        if vulnerability_group:
            parameters_found.append(
                cls.get_information(vulnerability_group)
            )

        if mobility_group:
            parameters_found.append(
                cls.get_information(mobility_group)
            )

        if immunization_group:
            parameters_found.append(
                cls.get_information(immunization_group)
            )

        if susceptibility_group:
            parameters_found.append(
                cls.get_information(susceptibility_group)
            )

        return parameters_found

    
    @classmethod
    def get_information(cls, parameter: Union[Document, Document]):
        """
        Gets the type and identifier of the parameter

        :param parameter: mongo document
        """
        data = BsonObject.dict(parameter,True).pop()

        return dict(
            variable=data["_cls"],
            identifier=data["identifier"]
        )
