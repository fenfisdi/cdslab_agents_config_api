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
    SusceptibilityGroupInterface,
    DistributionInterface,
    ConfigurationInterface
)
from src.models import (
    SusceptibilityGroup,
    NewSusceptibilityGroup,
    Distribution,
    NewDistribution
)
from src.utils.messages import (
    SusceptibilityGroupsMessages,
    ConfigurationMessage
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


susceptibility_groups_routes = APIRouter(tags=["SusceptibilityGroups"])


@susceptibility_groups_routes.get("/susceptibility_groups")
def find_all():
    """
    Get all existing susceptibility groups in db
    """
    try:
        susceptibility_groups = SusceptibilityGroupInterface.find_all()
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


@susceptibility_groups_routes.get(
    "/susceptibility_groups/{configuration_identifier}"
)
def find_by_configuration(
        configuration_identifier: str
):
    """
    Get existing susceptibility groups by configuration identifier

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

        mobility_groups = SusceptibilityGroupInterface.find_by_configuration(
            configuration
        )
        if not mobility_groups:
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
        BsonObject.dict(mobility_groups)
    )


@susceptibility_groups_routes.post(
    "/susceptibility_groups/{configuration_identifier}"
)
def create_mobility_group(
        configuration_identifier: str,
        susceptibility_groups: List[NewSusceptibilityGroup]
):
    """
    Created a mobility group in db

    \f
    :param configuration_identifier: Configuration Identifier
    :param susceptibility_groups: Mobility Groups list to insert in db
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

        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_susceptibility_group_entered,
                HTTP_400_BAD_REQUEST
            )

        susceptibility_groups_found = SusceptibilityGroupInterface.find_by_configuration(
            configuration
        )
        if susceptibility_groups_found:
            for susceptibility_group in susceptibility_groups_found:
                distribution_found = DistributionInterface.find_one(
                    susceptibility_groups_found.distribution.identifier
                )
                if distribution_found:
                    distribution_found.delete()
                susceptibility_group.delete()

        for susceptibility_group in susceptibility_groups:
            new_distribution = Distribution(
                **susceptibility_group.distribution.dict()
            )
            new_susceptibility_group = SusceptibilityGroup(
                **susceptibility_group.dict()
            )
            new_distribution.identifier = uuid.uuid1()
            new_distribution.save().reload()

            new_susceptibility_group.identifier = uuid.uuid1()
            new_susceptibility_group.configuration = configuration
            new_susceptibility_group.distribution = new_distribution
            new_susceptibility_group.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.created,
        HTTP_201_CREATED
    )
