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
        configuration_found = ConfigurationInterface.find_by_identifier(
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
def create_configuration(
    conf_uuid: UUID,
    immunization_groups: List[NewImmunizationGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a new immunization group in db.

    \f
    :param conf_uuid: Configuration identifier.
    :param immunization_groups: Immunization group list to insert.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
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
                ImmunizationGroupMessage.not_age_immunization_entered,
                HTTP_400_BAD_REQUEST
            )

        ig_found = ImmunizationGroupInterface.find_by_configuration(
            configuration_found
        )
        if ig_found:
            return UJSONResponse(
                ImmunizationGroupMessage.exist,
                HTTP_400_BAD_REQUEST
            )

        for immunization_group in immunization_groups:
            ImmunizationGroup(
                **immunization_group.dict(),
                identifier=uuid1(),
                configuration=configuration_found,
            ).save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.created,
        HTTP_201_CREATED
    )
