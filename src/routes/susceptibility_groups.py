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
    SusceptibilityGroupInterface
)
from src.models.db import SusceptibilityGroup
from src.models.route_models import (
    NewSusceptibilityGroup,
    UpdateSusceptibilityGroup
)
from src.use_case import SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ConfigurationMessage,
    SusceptibilityGroupMessages
)
from src.utils.response import UJSONResponse

susceptibility_groups_routes = APIRouter(tags=["Susceptibility Groups"])


@susceptibility_groups_routes.post(
    "/configuration/{conf_uuid}/susceptibility_groups"
)
def create_list_susceptibility_group(
    conf_uuid: UUID,
    susceptibility_groups: List[NewSusceptibilityGroup],
    user = Depends(SecurityUseCase.validate)
):
    """
    Created susceptibility groups from a list.

    \f
    :param conf_uuid: Configuration identifier.
    :param susceptibility_groups: Mobility Groups list to insert in db
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

        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupMessages.empty,
                HTTP_400_BAD_REQUEST
            )

        susceptibility_groups_found = SusceptibilityGroupInterface.find_by_conf(
            configuration,
        )
        if susceptibility_groups_found:
            return UJSONResponse(
                SusceptibilityGroupMessages.exist,
                HTTP_400_BAD_REQUEST
            )

        for susceptibility_group in susceptibility_groups:
            SusceptibilityGroup(
                **susceptibility_group.dict(),
                identifier=uuid1(),
                configuration=configuration
            ).save()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupMessages.created,
        HTTP_201_CREATED
    )


@susceptibility_groups_routes.post(
    "/configuration/{conf_uuid}/susceptibility_group"
)
def create_susceptibility_group(
    conf_uuid: UUID,
    susceptibility_group: NewSusceptibilityGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create susceptibility group from specific object.

    :param conf_uuid: Configuration identifier.
    :param susceptibility_group: Susceptibility group information to create.
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

        new_sg = SusceptibilityGroup(
            **susceptibility_group.dict(),
            configuration=configuration,
            identifier=uuid1()
        )
        new_sg.save().reload()

        return UJSONResponse(
            SusceptibilityGroupMessages.created,
            HTTP_201_CREATED,
            BsonObject.dict(new_sg)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@susceptibility_groups_routes.put(
    "/configuration/{conf_uuid}/susceptibility_group/{uuid}"
)
def update_susceptibility_group(
    conf_uuid: UUID,
    uuid: UUID,
    susceptibility_group: UpdateSusceptibilityGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update susceptibility group from specific configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: Susceptibility group uuid to update
    :param susceptibility_group: Susceptibility group information to update.
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
        sg_found = SusceptibilityGroupInterface.find_one(uuid)
        if not sg_found:
            return UJSONResponse(
                SusceptibilityGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )
        sg_found.update(**susceptibility_group.dict())
        sg_found.reload()

        return UJSONResponse(
            SusceptibilityGroupMessages.updated,
            HTTP_200_OK,
            BsonObject.dict(sg_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@susceptibility_groups_routes.get(
    "/configuration/{conf_uuid}/susceptibility_group/{uuid}"
)
def find_susceptibility_group(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find specific susceptibility group from a configuration.

    :param conf_uuid: Configuration identifier.
    :param uuid: Susceptibility group uuid to update.
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

        sg_found = SusceptibilityGroupInterface.find_one(uuid)
        if not sg_found:
            return UJSONResponse(
                SusceptibilityGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        return UJSONResponse(
            SusceptibilityGroupMessages.found,
            HTTP_200_OK,
            BsonObject.dict(sg_found)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_200_OK
        )


@susceptibility_groups_routes.get(
    "/configuration/{conf_uuid}/susceptibility_groups"
)
def list_susceptibility_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    List all susceptibility groups from a configuration.

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

        susceptibility_groups = SusceptibilityGroupInterface.find_by_conf(
            configuration
        )
        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupMessages.found,
        HTTP_200_OK,
        BsonObject.dict(susceptibility_groups)
    )


@susceptibility_groups_routes.delete(
    "/configuration/{conf_uuid}/susceptibility_group/{uuid}"
)
def delete_susceptibility_group(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
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

        sg_found = SusceptibilityGroupInterface.find_one(uuid)
        if not sg_found:
            return UJSONResponse(
                SusceptibilityGroupMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        sg_found.delete()
        return UJSONResponse(
            SusceptibilityGroupMessages.deleted,
            HTTP_200_OK
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )
