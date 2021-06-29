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
    MobilityGroupInterface,
UserInterface
)
from src.models.db import MobilityGroup
from src.models.route_models import NewMobilityGroup
from src.use_case import SecurityUseCase, DistributionUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ConfigurationMessage, MobilityGroupsMessages
from src.utils.response import UJSONResponse

mobility_group_routes = APIRouter(tags=["Mobility Groups"])


@mobility_group_routes.get("/configuration/{conf_uuid}/mobility_groups")
def list_mobility_groups(
    conf_uuid: UUID,
    user=Depends(SecurityUseCase.validate)
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
    user=Depends(SecurityUseCase.validate)
):
    """
    Create many mobility groups to specific configuration.

    \f
    :param conf_uuid: Configuration identifier
    :param mobility_groups: Mobility groups list to insert in db
    :param user: User logged
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
            DistributionUseCase.validateDistribution(
                mobility_group.distribution
            )
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


@mobility_group_routes.post("/configuration/{conf_uuid}/mobility_group")
def create_mobility_group(
    conf_uuid: UUID,
    mobility_group: NewMobilityGroup,
    user=Depends(SecurityUseCase.validate)
):
    """
        Create a mobility group to specific configuration.

        \f
        :param conf_uuid: Configuration identifier
        :param mobility_group: Mobility group to insert in db
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

        if not mobility_group:
            return UJSONResponse(
                MobilityGroupsMessages.not_distribution_entered,
                HTTP_400_BAD_REQUEST
            )

        DistributionUseCase.validateDistribution(
            mobility_group.distribution
        )
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


@mobility_group_routes.put(
    "/configuration/{conf_uuid}/mobility_group/{mob_uuid}"
)
def update_mobility_group(
    conf_uuid: UUID,
    mob_uuid: UUID,
    mobility_group: NewMobilityGroup,
    user=Depends(SecurityUseCase.validate)
):
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

        mobility_group_found = MobilityGroupInterface.find_one(mob_uuid)

        DistributionUseCase.validateDistribution(
            mobility_group.distribution
        )
        if not mobility_group_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_group_found.update(**mobility_group.dict())
        mobility_group_found.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.updated,
        HTTP_200_OK,
        BsonObject.dict(mobility_group_found)
    )


@mobility_group_routes.delete(
    "/configuration/{conf_uuid}/mobility_group/{mob_uuid}"
)
def update_mobility_group(
    conf_uuid: UUID,
    mob_uuid: UUID,
):
    try:
        user = UserInterface.find_one("diego@gmail.com")
        configuration = ConfigurationInterface.find_by_identifier(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_group_found = MobilityGroupInterface.find_one(mob_uuid)

        if not mobility_group_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_group_found.delete()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.deleted,
        HTTP_200_OK
    )
