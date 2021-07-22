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
    QuarantineGroupInterface,
    QuarantineInterface
)
from src.models.db import Quarantine, QuarantineGroup
from src.models.route_models import (
    NewQuarantine,
    UpdateQuarantine
)
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ConfigurationMessage,
    QuarantineGroupMessages,
    QuarantineMessage
)
from src.utils.response import UJSONResponse

quarantine_group_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Quarantine"]
)


@quarantine_group_routes.post("/quarantine")
def create_quarantine(
    conf_uuid: UUID,
    quarantine: NewQuarantine,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create quarantine groups to configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param quarantine: List of quarantine groups to save in db.
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        if not quarantine.quarantine_groups:
            return UJSONResponse(
                QuarantineGroupMessages.not_quarantine_groups_entered,
                HTTP_400_BAD_REQUEST
            )

        quarantine_found = QuarantineInterface.find_one_by_configuration(
            configuration
        )
        if not quarantine_found:
            quarantine_found = Quarantine(
                **quarantine.dict(exclude={'quarantine_groups'}),
                identifier=uuid1(),
                configuration=configuration
            )
            quarantine_found.save()

        for quarantine_group in quarantine.quarantine_groups:
            QuarantineGroup(
                **quarantine_group.dict(),
                identifier=uuid1(),
                quarantine=quarantine_found
            ).save()

        new_quarantine_groups = QuarantineGroupInterface.find_all(
            quarantine_found
        )

        new_quarantine_dict = BsonObject.dict(quarantine_found)
        new_quarantine_dict['quarantine_groups'] = BsonObject.dict(
            new_quarantine_groups
        )

        return UJSONResponse(
            QuarantineGroupMessages.created,
            HTTP_201_CREATED,
            new_quarantine_dict

        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@quarantine_group_routes.get("/quarantine")
def find_quarantine(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find quarantine from configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_found = QuarantineInterface.find_one_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        return UJSONResponse(
            QuarantineMessage.found,
            HTTP_200_OK,
            BsonObject.dict(quarantine_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@quarantine_group_routes.put("/quarantine")
def update_quarantine(
    conf_uuid: UUID,
    quarantine: UpdateQuarantine,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update quarantine information from configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param quarantine: Quarantine data to update.
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_found = QuarantineInterface.find_one_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_found.update(**quarantine.dict(exclude_none=True))
        quarantine_found.reload()

        return UJSONResponse(
            QuarantineMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(quarantine_found)
        )
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@quarantine_group_routes.get("/quarantine_group")
def list_quarantine_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find all existing quarantine groups from quarantine.

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """
    try:
        configuration = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_found = QuarantineInterface.find_one_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        qg_found = QuarantineGroupInterface.find_all(quarantine_found)

        return UJSONResponse(
            QuarantineGroupMessages.found,
            HTTP_200_OK,
            BsonObject.dict(qg_found)
        )
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
