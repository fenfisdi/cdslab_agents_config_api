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
    AgeGroupInterface,
    ConfigurationInterface
)
from src.models import (
    AgeGroup,
    NewAgeGroup
)
from src.utils.messages import (
    AgeGroupsMessages,
    ConfigurationMessage
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse

age_group_routes = APIRouter(tags=["AgeGroups"])


@age_group_routes.get("/age_groups")
def find_all():
    """
    Get all existing age groups in db
    """
    try:
        age_groups = AgeGroupInterface.find_all()

        if not age_groups:
            return UJSONResponse(
                AgeGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(age_groups)
    )


@age_group_routes.get("/age_groups/{configuration_identifier}")
def find_by_configuration(configuration_identifier: str):
    """
    Get existing age groups by configuration identifier

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

        age_groups = AgeGroupInterface.find_by_configuration(
            configuration
        )

        if not age_groups:
            return UJSONResponse(
                AgeGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(age_groups)
    )


@age_group_routes.post("/age_groups/{configuration_identifier}")
def create_age_groups(
        configuration_identifier: str,
        age_groups: List[NewAgeGroup]
):
    """
    Create age groups in db

    \f
    :param configuration_identifier: Identifier Configuration
    :param age_groups: List of age groups to save in db
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

        if not age_groups:
            return UJSONResponse(
                AgeGroupsMessages.not_age_groups_entry,
                HTTP_404_NOT_FOUND
            )

        age_groups_found = AgeGroupInterface.find_by_configuration(
            configuration
        )

        if age_groups_found:
            for age_group in age_groups_found:
                age_group.delete()

        for age_group in age_groups:
            new_age_group = AgeGroup(**age_group.dict())
            new_age_group.identifier = uuid.uuid1()
            new_age_group.configuration = configuration
            new_age_group.save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.created,
        HTTP_201_CREATED
    )
