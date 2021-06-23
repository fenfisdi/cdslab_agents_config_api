from typing import List
from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ConfigurationInterface
from src.interfaces.disease_group_interface import (
    DiseaseGroupsInterface,
    DiseaseStatesInterface
)
from src.models.db import DiseaseGroups
from src.models.route_models import NewDiseaseGroup
from src.use_case import SecurityUseCase
from src.utils import (
    BsonObject,
    ConfigurationMessage,
    DiseaseStatesMessage,
    UJSONResponse
)
from src.utils.messages import DiseaseGroupMessage

disease_states_routes = APIRouter(tags=["Disease States"])


@disease_states_routes.post('/configuration/{conf_uuid}/disease_states')
def create_disease_states(
    conf_uuid: UUID,
    disease_groups: List[NewDiseaseGroup],
    user = Depends(SecurityUseCase.validate)
):
    """

    :param conf_uuid:
    :param disease_groups:
    :param user:
    """

    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found = DiseaseGroupsInterface.find_all(configuration_found)
        if dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.exist,
                HTTP_400_BAD_REQUEST
            )

        if not disease_groups:
            return UJSONResponse(
                DiseaseGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        for disease_group in disease_groups:
            DiseaseGroups(
                **disease_group.dict(),
                identifier=uuid1(),
                configuration=configuration_found
            ).save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseGroupMessage.created,
        HTTP_201_CREATED
    )


@disease_states_routes.get('/configuration/{conf_uuid}/disease_states')
def create_disease_states(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found = DiseaseGroupsInterface.find_all(configuration_found)
        if not dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.not_found,
                HTTP_400_BAD_REQUEST
            )
        return UJSONResponse(
            DiseaseGroupMessage.found,
            HTTP_200_OK,
            BsonObject.dict(dg_found)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseGroupMessage.created,
        HTTP_201_CREATED
    )


@disease_states_routes.get("/diseaseStates")
def list_disease_states():
    """
    Get disease states in data base
    """
    try:
        states = DiseaseStatesInterface.find_all()

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
