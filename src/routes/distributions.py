from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import DistributionInterface
from src.models.general import DiseaseDistributionType
from src.utils import BsonObject, DistributionMessage, UJSONResponse

distributions_routes = APIRouter(tags=["Distributions"])


@distributions_routes.get("/distributions")
def list_distributions():
    """
    Get  all distributions
    """

    try:
        distributions = DistributionInterface.find_all()

        if not distributions:
            return UJSONResponse(
                DistributionMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        distributions_names = [
            data["name"] for data in BsonObject.dict(distributions)
        ]
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


@distributions_routes.get("/distributions/{name}/parameters")
def list_parameters(name: str):
    """
    Get  parameters for distribution name

    \f
    :param name: distribution name
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
    """Find disease state distribution"""

    return UJSONResponse(
        DistributionMessage.found,
        HTTP_200_OK,
        {state.name: state.value for state in DiseaseDistributionType}
    )
