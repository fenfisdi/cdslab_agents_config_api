from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.models.db import InitialPopulationSetup, Variables
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
