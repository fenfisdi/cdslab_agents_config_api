from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    ConfigurationInterface,
    DiseaseGroupsInterface,
    NaturalHistoryInterface,
    VulnerabilityGroupInterface
)
from src.models import NaturalHistory, NewNaturalHistory, UpdateNaturalHistory
from src.use_case import SecurityUseCase
from src.utils import BsonObject, UJSONResponse
from src.utils import NaturalHistoryMessage
from src.utils.messages import (
    ConfigurationMessage,
    DiseaseGroupMessage,
    VulnerabilityGroupMessage
)

natural_history_routes = APIRouter(tags=["Natural History"])


@natural_history_routes.post("/configuration/{conf_uuid}/natural_history")
def create_natural_history(
    conf_uuid: UUID,
    natural_history: NewNaturalHistory,
    user = Depends(SecurityUseCase.validate)
):
    """
    create a new natural history

    \f
    :param conf_uuid:
    :param natural_history: natural history information
    :param user:
    """
    try:
        config_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )
        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        vg_found = VulnerabilityGroupInterface.find_by_identifier(
            natural_history.vulnerability_group
        )
        if not vg_found:
            return UJSONResponse(
                VulnerabilityGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        dg_found = DiseaseGroupsInterface.find_one(
            natural_history.disease_group
        )
        if not dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        history = NaturalHistory(
            identifier=uuid1(),
            configuration=config_found,
            vulnerability_group=vg_found,
            disease_group=dg_found,
            **natural_history.dict(
                exclude={'vulnerability_group', 'disease_group'}
            )
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


@natural_history_routes.get("/configuration/{conf_uuid}/natural_history")
def list_natural_histories(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get a natural history that matches the id

    \f
    :param conf_uuid:
    :param user:
    """

    config_found = ConfigurationInterface.find_by_identifier(
        conf_uuid,
        user
    )
    if not config_found:
        return UJSONResponse(
            ConfigurationMessage.not_found,
            HTTP_404_NOT_FOUND
        )

    natural_history_found = NaturalHistoryInterface.find_by_config(
        config_found
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


# TODO: Verify Put Information
@natural_history_routes.put("/naturalHistory")
def update_configurate(natural_history: UpdateNaturalHistory):
    """
    Update a natural history

    \f
    :param natural_history: natural history information
    """

    try:
        natural_history_found = NaturalHistoryInterface.find_by_identifier(
            natural_history.identifier
        )

        if not natural_history_found:
            return UJSONResponse(
                NaturalHistoryMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        natural_history_found.update(
            **natural_history.dict(exclude_none=None)
        )

        natural_history_found.create_natural_history().reload()

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
