from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from src.utils.response import UJSONResponse
from src.utils.units import Units
from src.utils.messages import UnitsMessage

units_routes = APIRouter(tags=["units"])

@units_routes.get("/units/distance")
def units_distance():
    '''
        Get allowed distance units 
    '''
    return UJSONResponse(UnitsMessage.distance, HTTP_200_OK, Units.distance())

@units_routes.get("/units/time")
def units_time():
    '''
        Get allowed time units
    '''
    return UJSONResponse(UnitsMessage.time, HTTP_200_OK, Units.time())
