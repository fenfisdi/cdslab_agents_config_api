from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.utils.response import UJSONResponse
from src.utils.units import Units
from src.utils.messages import UnitsMessage

units_routes = APIRouter(tags=["units"])


@units_routes.get("/units/distance")
def units_distance():
    """
    Get allowed distance units 
    
    Return:
        Distance units configuration

    """
    try:
        distance = Units.distance()
        if distance is None:
            return UJSONResponse(
                UnitsMessage.distance_not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
    return UJSONResponse(
        UnitsMessage.distance,
        HTTP_200_OK,
        Units.distance()
    )


@units_routes.get("/units/time")
def units_time():
    """
    Get allowed time units 
    
    Return:
        Time units configuration

    """
    try:
        time = Units.time()
        if time is None:
            return UJSONResponse(
                UnitsMessage.time_not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
    return UJSONResponse(
        UnitsMessage.time,
        HTTP_200_OK,
        Units.time()
    )
