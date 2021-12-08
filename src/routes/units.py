from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.models.general import TracingVariables, UnitLength, UnitTime
from src.utils.messages import UnitsMessage
from src.utils.response import UJSONResponse

units_routes = APIRouter(tags=["Units"])


@units_routes.get("/units/distance")
def find_distance_units():
    """
    Get allowed distance units 
    """

    return UJSONResponse(
        UnitsMessage.distance,
        HTTP_200_OK,
        {unit.name: unit.value for unit in UnitLength}
    )


@units_routes.get("/units/time")
def find_time_units():
    """
    Get allowed time units 
    """

    return UJSONResponse(
        UnitsMessage.time,
        HTTP_200_OK,
        {unit.name: unit.value for unit in UnitTime}
    )


@units_routes.get("/quarantine/tracing")
def find_tracing_variables():
    """
    Find and return quarantine tracing variables.
    """
    return UJSONResponse(
        UnitsMessage.tracing,
        HTTP_200_OK,
        {unit.name: unit.value for unit in TracingVariables}
    )
