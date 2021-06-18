from uuid import UUID,uuid1
from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.utils import BsonObject, UJSONResponse
from src.utils import NaturalHistoryMessage
from src.models import NewNaturalHistory, NaturalHistory, \
    UpdateNaturalHistory
from src.use_case import NaturalHistoryUseCase
from src.interfaces import NaturalHistoryInterface

natural_history_routes = APIRouter(tags=["NaturalHistory"])

@natural_history_routes.post("/naturalHistory")
def save(natural_history: NewNaturalHistory):
    """
    create a new natural history

    \f
    :param natural_history: natural history information
    """
    try:    
        validated = NaturalHistoryUseCase.validate_parameters(
            config=natural_history.configuration,
            vulnerability_group=natural_history.vulnerability_group,
            disease_state=natural_history.disease_state
        )

        if isinstance(validated, str):
            return UJSONResponse(
                validated,
                HTTP_404_NOT_FOUND
            )

        history = NaturalHistory(
            identifier= uuid1(),
            configuration=validated["config"],
            vulnerability_group=validated["vulnerability_group"],
            disease_state=validated["disease_states"],
            distribution=natural_history.distribution,
            avoidance_radius=natural_history.avodance_radius,
            transitions=natural_history.transitions
        )
        history.save()
        
        return UJSONResponse(
            NaturalHistoryMessage.created,
            HTTP_201_CREATED,
            BsonObject.dict(history)
        )
    
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

@natural_history_routes.get("/naturalHistory/{uuid}")
def get_natural_history(id: UUID):
    """
    Get a natural history that matches the id

    \f
    :param id: natural history id
    """
    natural_history_found = NaturalHistoryInterface.find_by_identifier(
        id
    )

    if not natural_history_found:
        return UJSONResponse(
            NaturalHistoryMessage.not_found,
            HTTP_400_BAD_REQUEST
        )
    
    return UJSONResponse(
        NaturalHistoryMessage.found,
        HTTP_200_OK,
        BsonObject.dict(natural_history_found)
    )

@natural_history_routes.put("/naturalHistory")
def update_configurate(natural_history: UpdateNaturalHistory):
    """
    Update a natural history

    \f
    :param natural_history: natural history information
    """

    try:
        natural_history_found = NaturalHistoryInterface.find_by_identifier(
            natural_history.identiffer
        )

        if not natural_history_found:
            return UJSONResponse(
                NaturalHistoryMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        
        natural_history_found.update(
            **natural_history.dict(exclude_none=None)
        )

        natural_history_found.save().reload()

        return UJSONResponse(
            NaturalHistoryMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(natural_history_found)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
