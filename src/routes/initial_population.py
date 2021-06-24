from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.models.db import InitialPopulationSetup
from src.models.route_models import NewInitialPopulationSetup
from src.utils import (
    BsonObject,
    UJSONResponse, 
    InitialPopulationMessage,
    ConfigurationMessage
)
from src.use_case import InitialPopulationUseCase, SecurityUseCase
from src.interfaces import(
    ConfigurationInterface,
    InitialPopulationInterface
)

initial_population_routes = APIRouter(tags=["Initial Population"])

@initial_population_routes.get("/configuration/{conf_uuid}/initialPopulation/setup/variables")
def get_variables(
    config_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
):
    """
    Get all variables configured

    \f
    :param config_id: configuration id
    :param user: user information
    """

    try:
        parameters = InitialPopulationUseCase.find_parameters(config_uuid,user)

        return UJSONResponse(
            InitialPopulationMessage.found,
            HTTP_200_OK,
            parameters
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

@initial_population_routes.get("/configuration/{conf_uuid}/initialPopulation/setup")
def get_variables_config(
    config_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
):

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
        
        initial_population_found = InitialPopulationInterface.find_by_configuration(
            config_found
        )

        if not initial_population_found:
            return UJSONResponse(
                "",
                HTTP_200_OK,
                "AgeGroup"
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

        new_population = InitialPopulationSetup(
            identifier=uuid1(),
            configuration=config_found,
            **intial_population.dict()
        )

        new_population.save()

        return UJSONResponse(
            "",
            HTTP_201_CREATED,
            BsonObject.dict(new_population)
        )

        

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
