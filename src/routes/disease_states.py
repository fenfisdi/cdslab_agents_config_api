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
    DiseaseGroupInterface
)
from src.models.db import DiseaseGroup
from src.models.route_models import NewDiseaseGroup
from src.use_case import SecurityUseCase, VerifyDefaultState
from src.utils import (
    BsonObject,
    ConfigurationMessage,
    UJSONResponse
)
from src.utils.messages import DiseaseGroupMessage

disease_states_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Disease States"]
)


@disease_states_routes.post('/disease_states')
def create_disease_states(
    conf_uuid: UUID,
    disease_groups: List[NewDiseaseGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Save a list of disease states from specific configuration.

    :param conf_uuid: Identifier configuration
    :param disease_groups: Disease groups list
    :param user: User logged
    """

    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found = DiseaseGroupInterface.find_all(configuration_found)
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
            DiseaseGroup(
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


@disease_states_routes.get('/disease_state')
def list_disease_states(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    list all disease states from specific configuration.

    :param conf_uuid: Identifier configuration
    :param user: User logged
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        VerifyDefaultState.handle(configuration_found)

        dg_found = DiseaseGroupInterface.find_all(configuration_found)
        return UJSONResponse(
            DiseaseGroupMessage.found,
            HTTP_200_OK,
            BsonObject.dict(dg_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@disease_states_routes.post('/disease_state')
def create_disease_state(
    conf_uuid: UUID,
    disease_group: NewDiseaseGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Save a disease state from specific configuration.

    :param conf_uuid: Identifier configuration
    :param disease_group: Disease groups list
    :param user: User logged
    """

    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not disease_group:
            return UJSONResponse(
                DiseaseGroupMessage.not_entered,
                HTTP_404_NOT_FOUND
            )

        new_dg = DiseaseGroup(
            **disease_group.dict(),
            identifier=uuid1(),
            configuration=configuration_found
        )
        new_dg.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseGroupMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_dg)
    )


@disease_states_routes.put('/disease_state/{uuid}')
def update_disease_state(
    conf_uuid: UUID,
    uuid: UUID,
    disease_group: NewDiseaseGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update a disease state from specific configuration.

    :param conf_uuid: Identifier configuration
    :param uuid: Identifier disease state
    :param disease_group: Disease groups list
    :param user: User logged
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not disease_group:
            return UJSONResponse(
                DiseaseGroupMessage.not_entered,
                HTTP_404_NOT_FOUND
            )

        dg_found = DiseaseGroupInterface.find_one(uuid)

        if not dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found.update(**disease_group.dict(exclude_none=True))
        dg_found.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseGroupMessage.updated,
        HTTP_200_OK,
        BsonObject.dict(dg_found)
    )


@disease_states_routes.delete('/disease_state/{uuid}')
def delete_disease_state(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete a disease state from specific configuration.

    :param conf_uuid: Identifier configuration
    :param uuid: Identifier disease state
    :param user: User logged
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found = DiseaseGroupInterface.find_one(uuid)

        if not dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        dg_found.delete()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        DiseaseGroupMessage.deleted,
        HTTP_200_OK
    )
