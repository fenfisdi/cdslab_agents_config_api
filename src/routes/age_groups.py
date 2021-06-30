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
from src.models.db import AgeGroup
from src.models.route_models import NewAgeGroup, UpdateAgeGroup
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

    \f
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
    Create age groups in db.

    \f
    :param conf_uuid: Identifier Configuration.
    :param age_groups: List of age groups to save in db.
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

        if not age_groups:
            return UJSONResponse(
                AgeGroupsMessages.not_age_groups_entered,
                HTTP_404_NOT_FOUND
            )

        resp = []
        for age_group in age_groups:
            new_age_group = AgeGroup(
                **age_group.dict(),
                identifier=uuid1(),
                configuration=configuration
            )
            new_age_group.save().reload()
            resp.append(new_age_group)

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(resp)
    )


@age_group_routes.post("/configuration/{conf_uuid}/age_group")
def create_age_group(
    conf_uuid: UUID,
    age_group: NewAgeGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create age groups in db.

    \f
    :param conf_uuid: Identifier Configuration.
    :param age_group: Age group to save in db.
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

        if not age_group:
            return UJSONResponse(
                AgeGroupsMessages.not_age_groups_entered,
                HTTP_404_NOT_FOUND
            )

        new_age_group = AgeGroup(
            **age_group.dict(),
            identifier=uuid1(),
            configuration=configuration
        )
        new_age_group.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_age_group)
    )


@age_group_routes.put("/configuration/{conf_uuid}/age_group/{age_uuid}")
def update_age_group(
    conf_uuid: UUID,
    age_uuid: UUID,
    age_group: UpdateAgeGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update an age groups in db.

    \f
    :param conf_uuid: Identifier Configuration.
    :param age_uuid: Identifier age group.
    :param age_group: Age group to update in db.
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

        if not age_group:
            return UJSONResponse(
                AgeGroupsMessages.not_age_groups_entered,
                HTTP_404_NOT_FOUND
            )

        age_group_found = AgeGroupInterface.find_one(age_uuid)

        if not age_group_found:
            return UJSONResponse(
                AgeGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        age_group_found.update(**age_group.dict(exclude_none=True))
        age_group_found.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.created,
        HTTP_200_OK,
        BsonObject.dict(age_group_found)
    )


@age_group_routes.delete("/configuration/{conf_uuid}/age_group/{age_uuid}")
def update_age_group(
    conf_uuid: UUID,
    age_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete an age groups in db.

    \f
    :param conf_uuid: Identifier Configuration.
    :param age_uuid: Identifier age group.
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

        age_group_found = AgeGroupInterface.find_one(age_uuid)

        if not age_group_found:
            return UJSONResponse(
                AgeGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        age_group_found.delete()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        AgeGroupsMessages.deleted,
        HTTP_200_OK
    )
