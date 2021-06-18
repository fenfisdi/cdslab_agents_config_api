import uuid

from fastapi import APIRouter
from typing import List
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    QuarantineGroupInterface,
    ConfigurationInterface
)
from src.models import (
    NewQuarantineGroup,
    QuarantineGroup
)
from src.utils.messages import (
    QuarantineGroupsMessages,
    ConfigurationMessage
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


quarantine_group_routes = APIRouter(tags=["QuarantineGroups"])


@quarantine_group_routes.get("/quarantine_groups")
def find_all():
    """
    Get all existing quarantine groups in db
    """
    try:
        quarantine_groups = QuarantineGroupInterface.find_all()

        if not quarantine_groups:
            return UJSONResponse(
                QuarantineGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(quarantine_groups)
    )


@quarantine_group_routes.get(
    "/quarantine_groups/{configuration_identifier}"
)
def find_by_configuration(configuration_identifier: str):
    """
    Get all existing quarantine groups by configuration in db

    \f
    :param configuration_identifier: Configuration identifier to search
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

        quarantine_groups = QuarantineGroupInterface.find_by_configuration(
            configuration
        )

        if not quarantine_groups:
            return UJSONResponse(
                QuarantineGroupsMessages.not_found,
                HTTP_400_BAD_REQUEST
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(quarantine_groups)
    )


@quarantine_group_routes.post(
    "/quarantine_groups/{configuration_identifier}"
)
def create_quarantine_groups(
        configuration_identifier: str,
        quarantine_groups: List[NewQuarantineGroup]
):
    """
    Create quarantine groups in db

    :param configuration_identifier: Configuration Identifier to search
    :param quarantine_groups: List of quarantine groups to save in db
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

        if not quarantine_groups:
            return UJSONResponse(
                QuarantineGroupsMessages.not_quarantine_groups_entered,
                HTTP_400_BAD_REQUEST
            )

        quarantine_groups_found = QuarantineGroupInterface.find_by_configuration(
            configuration
        )
        if quarantine_groups_found:
            for quarantine_group in quarantine_groups_found:
                quarantine_group.delete()

        for quarantine_group in quarantine_groups:
            new_quarantine_group = QuarantineGroup(
                **quarantine_group.dict()
            )
            new_quarantine_group.identifier = uuid.uuid1()
            new_quarantine_group.configuration = configuration
            new_quarantine_group.save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupsMessages.created,
        HTTP_201_CREATED
    )
