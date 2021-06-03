from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.utils import (
        BsonObject,
        UJSONResponse
        ,DistributionMessage)

from src.interfaces import DistributionInterface

distributions_routes = APIRouter(tags=["distributions"])

@distributions_routes.get("/distributions")
def list_distributions():
    '''
        Get  all distributions
    '''
    distributions = DistributionInterface.find_all()

    if not distributions:
        return UJSONResponse(
        DistributionMessage.not_found, 
        HTTP_404_NOT_FOUND
        )  
      
    distributions_names = [data["name"] \
                for data in BsonObject.dict(distributions)]

    return UJSONResponse(
        DistributionMessage.found, 
        HTTP_200_OK,
        distributions_names
    )

@distributions_routes.get("/distributions/parameters/{name}")
def parameters(name: str):
    '''
        Get  parameters for distribution name
    '''
    parameters = DistributionInterface.find_parameters(name)

    if not parameters:
        return UJSONResponse(
        DistributionMessage.not_exist, 
        HTTP_400_BAD_REQUEST
        )  

    return UJSONResponse(
        DistributionMessage.found, 
        HTTP_200_OK,
        BsonObject.dict(parameters)
    )