from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.utils import UJSONResponse, InitialPopulationMessage
from src.use_case import InitialPopulationUseCase, SecurityUseCase


initial_population_routes = APIRouter(tags=["InitialPopulation"])

@initial_population_routes.get("/initialPopulation/setup")
def initial_population_setup(
    config_id: UUID,
    user=Depends(SecurityUseCase.validate)
):
    """
    Get all variables configured

    \f
    :param config_id: configuration id
    :param user: user information
    """

    try:
        parameters = InitialPopulationUseCase.find_parameters(config_id,user)

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
