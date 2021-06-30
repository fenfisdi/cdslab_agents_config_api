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
from src.models.route_models import NewQuarantine, UpdateQuarantineGroup
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ConfigurationMessage,
    QuarantineGroupMessages,
    QuarantineMessage
)
from src.utils.response import UJSONResponse

quarantine_group_routes = APIRouter(tags=["Quarantine"])


@quarantine_group_routes.get("/configuration/{conf_uuid}/quarantine_group")
def list_quarantine_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Get all existing quarantine groups in db
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

        quarantine_found = QuarantineInterface.find_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        qg_found = QuarantineGroupInterface.find_all(quarantine_found)

        if not qg_found:
            return UJSONResponse(
                QuarantineGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupMessages.found,
        HTTP_200_OK,
        BsonObject.dict(qg_found)
    )


@quarantine_group_routes.get("/configuration/{conf_uuid}/quarantine")
def find_quarantine(conf_uuid: UUID, user = Depends(SecurityUseCase.validate)):
    """
    Get all existing quarantine groups by configuration in db

    \f

    :param conf_uuid: Configuration identifier to search
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

        quarantine_found = QuarantineInterface.find_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineMessage.not_found,
                HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineMessage.found,
        HTTP_200_OK,
        BsonObject.dict(quarantine_found)
    )


@quarantine_group_routes.post("/configuration/{conf_uuid}/quarantine")
def create_quarantine(
    conf_uuid: UUID,
    quarantine: NewQuarantine,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create quarantine groups in db

    :param conf_uuid: Configuration Identifier to search
    :param quarantine: List of quarantine groups to save in db.
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

        if not quarantine.quarantine_groups:
            return UJSONResponse(
                QuarantineGroupMessages.not_quarantine_groups_entered,
                HTTP_400_BAD_REQUEST
            )

        quarantine_found = QuarantineInterface.find_by_configuration(
            configuration
        )
        if quarantine_found:
            return UJSONResponse(
                QuarantineGroupMessages.exist,
                HTTP_400_BAD_REQUEST
            )

        new_quarantine = Quarantine(
            **quarantine.dict(exclude={'quarantine_groups'}),
            identifier=uuid1(),
            configuration=configuration
        )
        new_quarantine.save().reload()

        for quarantine_group in quarantine.quarantine_groups:
            QuarantineGroup(
                **quarantine_group.dict(),
                identifier=uuid1(),
                quarantine=new_quarantine
            ).save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_quarantine)
    )


@quarantine_group_routes.put(
    "/configuration/{conf_uuid}/quarantine_group/{uuid}"
)
def update_quarantine_groups(
    conf_uuid: UUID,
    uuid: UUID,
    quarantine_group: UpdateQuarantineGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update quarantine group in db

    :param conf_uuid: Configuration Identifier to search
    :param uuid: Quarantine Group Identifier to search
    :param quarantine_group: Quarantine group to update in db.
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

        quarantine_found = QuarantineInterface.find_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_group_found = QuarantineGroupInterface.find_by_identifier(
            uuid
        )

        quarantine_group_found.update(
            **quarantine_group.dict()
        )
        quarantine_group_found.reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST,
        )
    return UJSONResponse(
        QuarantineGroupMessages.updated,
        HTTP_200_OK,
        BsonObject.dict(quarantine_group_found)
    )


@quarantine_group_routes.delete(
    "/configuration/{conf_uuid}/quarantine_group/{uuid}"
)
def delete_quarantine_group(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete quarantine group in db

    :param conf_uuid: Configuration Identifier to search
    :param uuid: Quarantine Group Identifier to search
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

        quarantine_found = QuarantineInterface.find_by_configuration(
            configuration
        )
        if not quarantine_found:
            return UJSONResponse(
                QuarantineGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_group_found = QuarantineGroupInterface.find_by_identifier(
            uuid
        )

        if not quarantine_group_found:
            return UJSONResponse(
                QuarantineGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_found.delete()
        quarantine_group_found.delete()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST,
        )
    return UJSONResponse(
        QuarantineGroupMessages.deleted,
        HTTP_200_OK
    )
