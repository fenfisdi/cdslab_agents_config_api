from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.models.db import InitialPopulationSetup, Variables
from src.models.general import ConfigurationVariableName
from src.models.route_models import NewInitialPopulationSetup
from src.utils import (
    BsonObject,
    UJSONResponse, 
    InitialPopulationMessage,
    ConfigurationMessage
)
from src.use_case import SecurityUseCase
from src.interfaces import(
    ConfigurationInterface,
    MobilityGroupInterface,
    DiseaseGroupsInterface,
    VulnerabilityGroupInterface,
    QuarantineGroupInterface,
    AgeGroupInterface,
    InitialPopulationInterface
)

initial_population_routes = APIRouter(tags=["Initial Population"])

@initial_population_routes.get("/configuration/{conf_uuid}/initialPopulation/setup/variables")
def get_variables(
    config_uuid: UUID,
    configurated: bool,
    user=Depends(SecurityUseCase.validate)
):
    """
    Get all variables

    \f
    :param config_id: configuration id
    :param user: user information
    :param configurated: get variables configured
    """

    try:
        variables = ConfigurationInterface.find_variables(
            config_uuid,
            user,
            configurated
        )
        
        return UJSONResponse(
            InitialPopulationMessage.found,
            HTTP_200_OK,
            variables
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@initial_population_routes.get("/configuration/{conf_uuid}/initialPopulation/setup/parameters")
def get_parameters(
    config_uuid: UUID,
    variable: ConfigurationVariableName,
    user=Depends(SecurityUseCase.validate)
):
    """
    
    Get the parameters for each variable name

    \f
    :param config_uuid: configuration id
    :param variable: configured variable
    :param user: user information
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            config_uuid,
            user
        )

        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if variable is ConfigurationVariableName.mobility:
            parameter = MobilityGroupInterface.find_by_configuration(config_found)
        elif variable is ConfigurationVariableName.disease:
            parameter = DiseaseGroupsInterface.find_all(config_found)
        elif variable is ConfigurationVariableName.vulnerability:
            parameter = VulnerabilityGroupInterface.find_by_configuration(config_found)
        elif variable is ConfigurationVariableName.quaratine:
            parameter = QuarantineGroupInterface.find_by_configuration(config_found)
        elif variable is ConfigurationVariableName.Age:
            parameter = AgeGroupInterface.find_by_configuration
        else:
            return UJSONResponse(
                InitialPopulationMessage.not_found,
                HTTP_400_BAD_REQUEST
            )

        return UJSONResponse(
            InitialPopulationMessage.parameters_found,
            HTTP_200_OK,
            BsonObject.dict(parameter)
        )


    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@initial_population_routes.get(
    "/configuration/{conf_uuid}/initialPopulation/setup/{uuid}"
)
def get_initial_population_setup(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get a initial population

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: initial identifier.
    :param user: User authenticated.
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        ip_found = InitialPopulationInterface.find_one(uuid)

        if not ip_found:
            return UJSONResponse(
                InitialPopulationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        return UJSONResponse(
            InitialPopulationMessage.setup_found,
            HTTP_200_OK,
            BsonObject.dict(ip_found)
        )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
        

@initial_population_routes.post("/configuration/{conf_uuid}/initialPopulation/setup")
def create_initial_population_setup(
    config_uuid: UUID,
    intial_population: NewInitialPopulationSetup,
    user=Depends(SecurityUseCase.validate)
):
    """
    
    Get the parameters for each variable name

    \f
    :param config_uuid: configuration id
    :param initial_population: initial population information
    :param user: user information
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            config_uuid,
            user
        )

        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        
        variables=[
                Variables(
                    name=variable.name.value,
                    configured=True if variable.name == intial_population.variable_name else variable.configured
                )
                for variable in config_found.variables 
        ]

        config_found.update(variables=variables)
        config_found.save().reload()

        new_population = InitialPopulationSetup(
            identifier=uuid1(),
            configuration=config_found,
            **intial_population.dict(exclude={'variable_name'})
        )

        new_population.save()

        return UJSONResponse(
            ConfigurationMessage.created,
            HTTP_201_CREATED,
            BsonObject.dict(new_population)
        )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@initial_population_routes.put(
    "/configuration/{conf_uuid}/initialPopulation/setup/{uuid}"
)
def update_initial_population_setup(
    conf_uuid: UUID,
    uuid: UUID,
    initial_population: NewInitialPopulationSetup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Updated a initial population

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: initial population identifier.
    :param initial_population: initial population to update.
    :param user: User authenticated.
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        ip_found = InitialPopulationInterface.find_one(uuid)

        if not ip_found:
            return UJSONResponse(
                InitialPopulationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        ip_found.update(**initial_population.dict(exclude={'variable_name'}))
        ip_found.reload()

        return UJSONResponse(
            InitialPopulationMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(ip_found)
        )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@initial_population_routes.delete(
    "/configuration/{conf_uuid}/initialPopulation/setup/{uuid}"
)
def delete_initial_population_setup(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete a initial population

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: initial identifier.
    :param user: User authenticated.
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        ip_found = InitialPopulationInterface.find_one(uuid)

        if not ip_found:
            return UJSONResponse(
                InitialPopulationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        ip_found.delete()
        return UJSONResponse(
            InitialPopulationMessage.deleted,
            HTTP_200_OK
        )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
