import uuid
from typing import List

from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    MobilityGroupInterface,
    DistributionInterface,
    ConfigurationInterface
)
from src.models import (
    MobilityGroup,
    Distribution,
    NewMobilityGroup,
    NewDistribution
)
from src.utils.messages import (
    MobilityGroupsMessages,
    ConfigurationMessage
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


mobility_group_routes = APIRouter(tags=["MobilityGroups"])


@mobility_group_routes.get("/mobility_groups")
def find_all():
    """
    Get all existing mobility group in db
    """
    try:
        mobility_groups = MobilityGroupInterface.find_all()
        if not mobility_groups:
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
        BsonObject.dict(mobility_groups)
    )


@mobility_group_routes.get(
    "/mobility_groups/{configuration_identifier}"
)
def find_by_configuration(
        configuration_identifier: str
):
    """
    Get existing mobility groups by configuration identifier

    \f
    :param configuration_identifier: Configuration identifier
    """
    try:
        configuration = ConfigurationInterface.find_by_identifier(
            configuration_identifier
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_groups = MobilityGroupInterface. \
            find_by_configuration(configuration)

        if not mobility_groups:
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
        BsonObject.dict(mobility_groups)
    )


@mobility_group_routes.post(
    "/mobility_groups/{configuration_identifier}"
)
def create_mobility_group(
        configuration_identifier: str,
        mobility_groups: List[NewMobilityGroup]
):
    """
    Create a mobility group in db

    :param configuration_identifier: Configuration identifier
    :param mobility_groups: Mobility groups list to insert in db
    """
    try:
        configuration = ConfigurationInterface.find_by_identifier(
            configuration_identifier
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

        mobility_groups_found = MobilityGroupInterface.find_by_configuration(
            configuration
        )

        if mobility_groups_found:
            for mobility_group in mobility_groups_found:
                distribution_found = DistributionInterface.find_one(
                    mobility_group.distribution.identifier
                )
                if distribution_found:
                    distribution_found.delete()
                mobility_group.delete()

        for mobility_group in mobility_groups:
            new_distribution = Distribution(
                **mobility_group.distribution.dict()
            )
            new_mobility_group = MobilityGroup(
                **mobility_group.dict()
            )
            new_distribution.identifier = uuid.uuid1()
            new_distribution.save().reload()

            new_mobility_group.identifier = uuid.uuid1()
            new_mobility_group.configuration = configuration
            new_mobility_group.distribution = new_distribution
            new_mobility_group.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.created,
        HTTP_201_CREATED
    )
