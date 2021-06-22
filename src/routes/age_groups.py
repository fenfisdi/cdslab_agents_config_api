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
    AgeGroupInterface,
    ConfigurationInterface
)
from src.models import (
    AgeGroup,
    NewAgeGroup
)
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import (
    AgeGroupsMessages,
    ConfigurationMessage
)
from src.utils.response import UJSONResponse

age_group_routes = APIRouter(tags=["Age Groups"])


@age_group_routes.get("/configuration/{conf_uuid}/age_groups")
def list_age_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get existing age groups by configuration identifier.

    :param conf_uuid: Configuration identifier.
    :param user: User Authenticated.
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


@age_group_routes.post("/configuration/{conf_uuid}/age_groups")
def create_age_groups(
    conf_uuid: UUID,
    age_groups: List[NewAgeGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Create age groups in db

    \f
    :param conf_uuid: Identifier Configuration.
    :param age_groups: List of age groups to save in db.
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

        if not age_groups:
            return UJSONResponse(
                AgeGroupsMessages.not_age_groups_entered,
                HTTP_404_NOT_FOUND
            )

        age_groups_found = AgeGroupInterface.find_by_configuration(
            configuration
        )

        if age_groups_found:
            for age_group in age_groups_found:
                age_group.delete()

        for age_group in age_groups:
            new_age_group = AgeGroup(
                **age_group.dict(),
                identifier=uuid1(),
                configuration=configuration
            )
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
