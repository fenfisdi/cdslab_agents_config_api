from typing import List, Union
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
    SusceptibilityGroupInterface
)
from src.models.db import SusceptibilityGroup
from src.models.route_models import NewSusceptibilityGroup
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ConfigurationMessage,
    SusceptibilityGroupMessages
)
from src.utils.response import UJSONResponse

susceptibility_groups_routes = APIRouter(tags=["Susceptibility Groups"])


@susceptibility_groups_routes.get(
    "/configuration/{conf_uuid}/susceptibility_groups"
)
def find_susceptibility_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get existing susceptibility groups by configuration identifier

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        susceptibility_groups = SusceptibilityGroupInterface.find_by_conf(
            configuration
        )
        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(susceptibility_groups)
    )


@susceptibility_groups_routes.post(
    "/configuration/{conf_uuid}/susceptibility_groups"
)
def create_susceptibility_group(
    conf_uuid: UUID,
    susceptibility_groups: List[NewSusceptibilityGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Created a mobility group in db

    \f
    :param conf_uuid: Configuration Identifier
    :param susceptibility_groups: Mobility Groups list to insert in db
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_susceptibility_group_entered,
                HTTP_400_BAD_REQUEST
            )

        susceptibility_groups_found = SusceptibilityGroupInterface.find_by_conf(
            configuration,
        )
        if susceptibility_groups_found:
            return UJSONResponse(
                SusceptibilityGroupsMessages.exist,
                HTTP_400_BAD_REQUEST
            )

        for susceptibility_group in susceptibility_groups:
            SusceptibilityGroup(
                **susceptibility_group.dict(),
                identifier=uuid1(),
                configuration=configuration
            ).save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.created,
        HTTP_201_CREATED
    )
