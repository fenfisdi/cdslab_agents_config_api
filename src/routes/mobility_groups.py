from typing import List
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
    MobilityGroupInterface
)
from src.models.db import MobilityGroup
from src.models.route_models import NewMobilityGroup
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ConfigurationMessage, MobilityGroupsMessages
from src.utils.response import UJSONResponse

mobility_group_routes = APIRouter(tags=["Mobility Groups"])


@mobility_group_routes.get("/configuration/{conf_uuid}/mobility_groups")
def list_mobility_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    List all mobility groups from specific configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param user:
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

        mobility_groups_found = MobilityGroupInterface.find_by_configuration(
            configuration
        )

        if not mobility_groups_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(mobility_groups_found)
    )


@mobility_group_routes.post("/configuration/{conf_uuid}/mobility_groups")
def create_mobility_groups(
    conf_uuid: UUID,
    mobility_groups: List[NewMobilityGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a mobility groups to specific configuration.

    \f
    :param conf_uuid: Configuration identifier
    :param mobility_groups: Mobility groups list to insert in db
    :param user:
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

        if not mobility_groups:
            return UJSONResponse(
                MobilityGroupsMessages.not_distribution_entered,
                HTTP_400_BAD_REQUEST
            )

        for mobility_group in mobility_groups:
            MobilityGroup(
                **mobility_group.dict(),
                identifier=uuid1(),
                configuration=configuration,
            ).save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.created,
        HTTP_201_CREATED
    )
