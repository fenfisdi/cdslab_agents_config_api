from uuid import UUID, uuid1

from fastapi import APIRouter, Depends, File, UploadFile
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    ConfigurationInterface,
    MobilityGroupInterface
)
from src.models.db import MobilityGroup
from src.models.route_models import NewMobilityGroup
from src.use_case import SaveDistributionFile, SecurityUseCase, VerifyDistributionFile
from src.utils.encoder import BsonObject
from src.utils.messages import ConfigurationMessage, DistributionMessage, MobilityGroupsMessages
from src.utils.response import UJSONResponse

mobility_group_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Mobility Groups"]
)


@mobility_group_routes.get("/mobility_group")
def list_mobility_groups(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    List all mobility groups from specific configuration.

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

        mg_found = MobilityGroupInterface.find_all_by_conf(
            configuration
        )

        return UJSONResponse(
            MobilityGroupsMessages.found,
            HTTP_200_OK,
            BsonObject.dict(mg_found)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@mobility_group_routes.post("/mobility_group")
def create_mobility_group(
    conf_uuid: UUID,
    mobility_group: NewMobilityGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a mobility group to specific configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param mobility_group: Mobility group to insert in db.
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

        new_mobility_group = MobilityGroup(
            **mobility_group.dict(),
            identifier=uuid1(),
            configuration=configuration,
        )
        new_mobility_group.save().reload()

        return UJSONResponse(
            MobilityGroupsMessages.created,
            HTTP_201_CREATED,
            BsonObject.dict(new_mobility_group)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@mobility_group_routes.get("/mobility_group/{uuid}")
def find_mobility_group(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find mobility group from specific configuration.

    \f
    :param conf_uuid: Configuration identifier
    :param uuid: MobilityGroup identifier
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

        mg_found = MobilityGroupInterface.find_one_by_id(uuid)
        if not mg_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
        return UJSONResponse(
            MobilityGroupsMessages.found,
            HTTP_404_NOT_FOUND,
            BsonObject.dict(mg_found)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@mobility_group_routes.put("/mobility_group/{uuid}")
def update_mobility_group(
    conf_uuid: UUID,
    uuid: UUID,
    mobility_group: NewMobilityGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update a mobility group to specific configuration.

    \f
    :param conf_uuid: Configuration identifier
    :param uuid: MobilityGroup identifier
    :param mobility_group: Mobility group to update in db
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

        mobility_group_found = MobilityGroupInterface.find_one_by_id(uuid)

        if not mobility_group_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_group_found.update(**mobility_group.dict(exclude_none=True))
        mobility_group_found.save().reload()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.updated,
        HTTP_200_OK,
        BsonObject.dict(mobility_group_found)
    )


@mobility_group_routes.delete("/mobility_group/{uuid}")
def delete_mobility_group(
    conf_uuid: UUID,
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete a mobility group to specific configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: MobilityGroup identifier.
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

        mobility_group_found = MobilityGroupInterface.find_one_by_id(uuid)

        if not mobility_group_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        mobility_group_found.delete()

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.deleted,
        HTTP_200_OK
    )


@mobility_group_routes.put("/mobility_group/{uuid}/file")
def update_distribution_file(
    conf_uuid: UUID,
    uuid: UUID,
    file: UploadFile = File(...),
    user = Depends(SecurityUseCase.validate)
):
    """
    Update file distribution to a mobility group.

    \f
    :param conf_uuid: Configuration identifier.
    :param uuid: MobilityGroup identifier.
    :param user: User authenticated.
    :param file: File associated to distribution mobility group.
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

        mg_found = MobilityGroupInterface.find_one_by_id(uuid)

        if not mg_found:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )

        is_valid = VerifyDistributionFile.simple(
            file,
            mg_found
        )
        if not is_valid:
            return UJSONResponse(
                DistributionMessage.invalid,
                HTTP_400_BAD_REQUEST
            )

        data, is_invalid = SaveDistributionFile.handle(
            file,
            configuration,
            mg_found.name
        )
        if is_invalid:
            return UJSONResponse(
                DistributionMessage.can_not_save,
                HTTP_400_BAD_REQUEST
            )
        mg_found.distribution.file_id = data.get('id')
        mg_found.save().reload()

        return UJSONResponse(
            DistributionMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(mg_found)
        )

    except Exception as error:
        return UJSONResponse(str(error),HTTP_400_BAD_REQUEST)
