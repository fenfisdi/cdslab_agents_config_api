from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.general import UnitLength, UnitTime
from src.utils.messages import UnitsMessage
from src.utils.response import UJSONResponse

units_routes = APIRouter(tags=["Units"])


@units_routes.get("/units/distance")
def units_distance():
    """
    Get allowed distance units 
    """

    return UJSONResponse(
        UnitsMessage.distance,
        HTTP_200_OK,
        {unit.name: unit.value for unit in UnitLength}
    )


@units_routes.get("/units/time")
def units_time():
    """
    Get allowed time units 
    """

    return UJSONResponse(
        UnitsMessage.time,
        HTTP_200_OK,
        {unit.name: unit.value for unit in UnitTime}
    )
