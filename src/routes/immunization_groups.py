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
    ImmunizationGroupInterface
)
from src.models.db import ImmunizationGroup
from src.models.route_models import NewImmunizationGroup
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ConfigurationMessage, ImmunizationGroupMessage
from src.utils.response import UJSONResponse

immunization_routes = APIRouter(tags=["Immunization Groups"])


@immunization_routes.get("/configuration/{conf_uuid}/immunization_groups")
def list_immunization_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get all existing immunization groups by configuration in db.

    \f
    :param conf_uuid: Configuration Identifier to find.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
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


@immunization_routes.post("/configuration/{conf_uuid}/immunization_groups")
def create_immunization_groups(
    conf_uuid: UUID,
    immunization_groups: List[NewImmunizationGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a list of new immunization group in db.

    \f
    :param conf_uuid: Configuration identifier.
    :param immunization_groups: Immunization group list to insert.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not immunization_groups:
            return UJSONResponse(
                ImmunizationGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        res = []
        for immunization_group in immunization_groups:
            img = ImmunizationGroup(
                **immunization_group.dict(),
                identifier=uuid1(),
                configuration=configuration_found,
            )
            img.save().reload()
            res.append(img)

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(res)
    )


@immunization_routes.post("/configuration/{conf_uuid}/immunization_group")
def create_immunization_group(
    conf_uuid: UUID,
    immunization_group: NewImmunizationGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a new immunization group in db.

    \f
    :param conf_uuid: Configuration identifier.
    :param immunization_group: Immunization group to insert.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not immunization_group:
            return UJSONResponse(
                ImmunizationGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        img = ImmunizationGroup(
            **immunization_group.dict(),
            identifier=uuid1(),
            configuration=configuration_found,
        )
        img.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ImmunizationGroupMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(img)
    )


@immunization_routes.put(
    "/configuration/{conf_uuid}/immunization_group/{img_uuid}"
)
def update_immunization_group(
    conf_uuid: UUID,
    img_uuid: UUID,
    immunization_group: NewImmunizationGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update a new immunization group in db.

    \f
    :param conf_uuid: Configuration identifier.
    :param img_uuid: Immunization group identifier.
    :param immunization_group: Immunization group to insert.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not immunization_group:
            return UJSONResponse(
                ImmunizationGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        img_found = ImmunizationGroupInterface.find_one(img_uuid)
        if not img_found:
            return UJSONResponse(
                ImmunizationGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        img_found.update(**immunization_group.dict(exclude_none=True))
        img_found.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ImmunizationGroupMessage.updated,
        HTTP_200_OK,
        BsonObject.dict(img_found)
    )


@immunization_routes.delete(
    "/configuration/{conf_uuid}/immunization_group/{img_uuid}"
)
def delete_immunization_group(
    conf_uuid: UUID,
    img_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete a new immunization group in db.

    \f
    :param conf_uuid: Configuration identifier.
    :param img_uuid: Immunization group identifier.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        img_found = ImmunizationGroupInterface.find_one(img_uuid)
        if not img_found:
            return UJSONResponse(
                ImmunizationGroupMessage.not_entered,
                HTTP_400_BAD_REQUEST
            )

        img_found.delete()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ImmunizationGroupMessage.deleted,
        HTTP_200_OK
    )
