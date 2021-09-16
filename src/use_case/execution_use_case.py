from typing import List
from uuid import UUID

from src.interfaces import (
    AgeGroupInterface,
    DiseaseGroupInterface,
    MobilityGroupInterface,
    NaturalHistoryInterface,
    QuarantineGroupInterface,
    QuarantineInterface,
    SusceptibilityGroupInterface,
    VulnerabilityGroupInterface
)
from src.models.db import Configuration, User
from src.services import CloudAPI
from src.utils.encoder import BsonObject
from .security_use_case import SecurityUseCase


class FindAgentInformation:

    @classmethod
    def handle(cls, configuration: Configuration) -> dict:
        configuration_dict = dict(
            configuration=cls._get_configuration(configuration),
            age_groups=cls._get_age_groups(configuration),
            mobility_groups=cls._get_mobility_groups(configuration),
            susceptibility_groups=cls._get_susceptibility_groups(configuration),
            vulnerability_groups=cls._get_vulnerability_groups(configuration),
            disease_groups=cls._get_disease_groups(configuration),
            natural_history=cls._get_natural_history(configuration),
            quarantine=cls._get_quarantine(configuration),
            quarantine_groups=cls._get_quarantine_groups(configuration)
        )
        return configuration_dict

    @classmethod
    def _get_age_groups(cls, configuration: Configuration) -> List[dict]:
        age_groups = AgeGroupInterface.find_all_by_conf(configuration)
        return BsonObject.dict(age_groups)

    @classmethod
    def _get_mobility_groups(cls, configuration: Configuration) -> List[dict]:
        mobility_groups = MobilityGroupInterface.find_all_by_conf(configuration)
        return BsonObject.dict(mobility_groups)

    @classmethod
    def _get_susceptibility_groups(
        cls,
        configuration: Configuration
    ) -> List[dict]:
        susceptibility_groups = SusceptibilityGroupInterface.find_all_by_conf(
            configuration
        )
        return BsonObject.dict(susceptibility_groups)

    @classmethod
    def _get_vulnerability_groups(
        cls,
        configuration: Configuration
    ) -> List[dict]:
        vulnerability_groups = VulnerabilityGroupInterface.find_all_by_conf(
            configuration
        )
        return BsonObject.dict(vulnerability_groups)

    @classmethod
    def _get_disease_groups(
        cls,
        configuration: Configuration
    ) -> List[dict]:
        disease_group = DiseaseGroupInterface.find_all_by_conf(configuration)
        return BsonObject.dict(disease_group)

    @classmethod
    def _get_natural_history(
        cls,
        configuration: Configuration
    ) -> List[dict]:
        natural_history = NaturalHistoryInterface.find_all_by_config(
            configuration
        )
        return BsonObject.dict(natural_history)

    @classmethod
    def _get_quarantine(cls, configuration: Configuration) -> dict:
        quarantine = QuarantineInterface.find_one_by_conf(configuration)
        return BsonObject.dict(quarantine)

    @classmethod
    def _get_quarantine_groups(cls, configuration: Configuration) -> List[dict]:
        quarantine_group = QuarantineGroupInterface.find_all_by_conf(
            configuration
        )
        return BsonObject.dict(quarantine_group)

    @classmethod
    def _get_configuration(cls, configuration: Configuration) -> dict:
        return BsonObject.dict(configuration)


class FindMachineInformation:

    @classmethod
    def handle(cls, user: User) -> dict:

        data = {
            'cpu': 2,
            'memory': 2048,
            'instances': 5,
        }

        if user.role and user.role.value == 'admin':
            data['instances'] = 10

        return data


class SendAllInformation:

    @classmethod
    def handle(
        cls,
        configuration: UUID,
        user: User,
        simulation_data: dict,
        machine_data: dict
    ) -> bool:
        token = SecurityUseCase.create_token(user)
        data = {
            'data': simulation_data,
            'machine': machine_data,
            'simulation_id': str(configuration)
        }
        _, is_invalid = CloudAPI.execute_simulation(data, token)
        return is_invalid
