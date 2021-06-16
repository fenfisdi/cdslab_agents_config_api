from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)

from src.interfaces.disease_states_interface import DiseaseStatesInterface
from src.utils import (
    BsonObject,
    UJSONResponse,
    DiseaseStatesMessage
)

disease_states_routes = APIRouter(tags=["DiseaseStates"])


@disease_states_routes.get("/diseaseStates")
def list_disease_states():
    """
    Get disease states in data base
    """
    try:
        states = DiseaseStatesInterface.fin_all()

        if not states:
            return UJSONResponse(
                DiseaseStatesMessage.not_found,
                HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseStatesMessage.found,
        HTTP_200_OK,
        BsonObject.dict(states)
    )
