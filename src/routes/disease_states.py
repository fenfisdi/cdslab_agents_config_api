from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

from src.interfaces.disease_states_interface import DiseaseStatesInterface
from src.utils import (
        BsonObject,
        UJSONResponse,
        DiseaseStatesMessage
        )

disease_states_routes = APIRouter(tags=["DiseaseStates"])

@disease_states_routes.get("/DiseaseStates")
def list_disease_states():
    
    states = DiseaseStatesInterface.fin_all()

    if not states:    
        return UJSONResponse(
            DiseaseStatesMessage.not_found,
            HTTP_404_NOT_FOUND
        )

    return UJSONResponse(
        DiseaseStatesMessage.found,
        HTTP_200_OK,
        BsonObject.dict(states)
    )
