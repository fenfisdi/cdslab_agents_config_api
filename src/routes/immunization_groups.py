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
    ImmunizationGroupInterface,
    ConfigurationInterface,
    DistributionInterface
)
from src.models import (
    NewImmunizationGroup,
    Distribution,
    ImmunizationGroup
)
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ImmunizationGroupMessage,
    ConfigurationMessage
)
from src.utils.response import UJSONResponse


immunization_routes = APIRouter(tags=["ImmunizationGroups"])


@immunization_routes.get("/immunization_groups/{uuid}")
def list_immunization_groups(uuid: UUID):
    """
    Get all existing immunization groups by configuration in db.

    \f
    :param uuid: Configuration Identifier to find.
    """
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
            uuid
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        immunization_groups = ImmunizationGroupInterface.find_by_configuration(
            configuration_found
        )
        if not immunization_groups:
            return UJSONResponse(
                ImmunizationGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ImmunizationGroupMessage.found,
        HTTP_200_OK,
        BsonObject.dict(immunization_groups)
    )


@immunization_routes.post("/immunization_groups/{uuid}")
def create_configuration(
        uuid: UUID,
        immunization_groups: List[NewImmunizationGroup]
):
    """
    Create a new immunization group in db.

    \f
    :param uuid: Configuration identifier.
    :param immunization_groups: Immunization group list to insert.
    """
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
            uuid
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not immunization_groups:
            return UJSONResponse(
                ImmunizationGroupMessage.not_age_immunization_entered,
                HTTP_400_BAD_REQUEST
            )

        immunization_groups_found = ImmunizationGroupInterface.find_by_configuration(
            configuration_found
        )
        if immunization_groups_found:
            for immunization_group in immunization_groups_found:
                distribution_found = DistributionInterface.find_one(
                    immunization_group.distribution.identifier
                )
                if distribution_found:
                    distribution_found.delete()
                immunization_group.delete()

        for immunization_group in immunization_groups:
            new_distribution = Distribution(
                **immunization_group.distribution.dict(),
                identifier=uuid1()
            ).save().reload()
            new_immunization_group = ImmunizationGroup(
                name=immunization_group.name,
                identifier=uuid1(),
                configuration=configuration_found,
                distribution=new_distribution
            )
            new_immunization_group.save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.created,
        HTTP_201_CREATED
    )
