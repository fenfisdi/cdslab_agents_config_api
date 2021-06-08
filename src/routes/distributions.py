from fastapi import APIRouter
from starlette.status import HTTP_200_OK, \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.utils import BsonObject, \
    UJSONResponse, DistributionMessage
from src.interfaces.distribution_interface import DistributionInterface

from src.interfaces import DistributionInterface
from src.utils.disease_state_distributio import DiseaseStatesDistribution

distributions_routes = APIRouter(tags=["distributions"])


@distributions_routes.get("/distributions")
def list_distributions():
    """
    Get  all distributions

    Return:
        Distribution object list

    """

    try:
        distributions = DistributionInterface.find_all()

        if not distributions:
            return UJSONResponse(
                DistributionMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        distributions_names = [data["name"] \
                               for data in BsonObject.dict(distributions)]
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DistributionMessage.found,
        HTTP_200_OK,
        distributions_names
    )


@distributions_routes.get("/distributions/parameters/{name}")
def parameters(name: str):
    """
    Get  parameters for distribution name

    Return:
        Distribution parameters object

    """
    try:
        parameters = DistributionInterface.find_parameters(name)

        if not parameters:
            return UJSONResponse(
                DistributionMessage.not_exist,
                HTTP_400_BAD_REQUEST
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DistributionMessage.found,
        HTTP_200_OK,
        BsonObject.dict(parameters)
    )


@distributions_routes.get("/distributions/disease_state")
def list_disease_state_distribution():
    """
    Get disease states distribution list

    Return:
        Disease state distributions object list

    """
    try:
        disease_states_distribution = DiseaseStatesDistribution.get_disease_states_distribution()

        if not disease_states_distribution:
            return UJSONResponse(
                DistributionMessage.not_exist,
                HTTP_400_BAD_REQUEST
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DistributionMessage.disease_states_distribution_found,
        HTTP_200_OK,
        BsonObject.dict(disease_states_distribution)
    )
