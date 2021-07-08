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
    SusceptibilityGroupInterface
)
from src.models.db import SusceptibilityGroup
from src.models.route_models import (
    NewSusceptibilityGroup,
    UpdateSusceptibilityGroup
)
from src.use_case import SaveDistributionFile, SecurityUseCase, VerifySimpleDistributionFile
from src.utils.encoder import BsonObject
from src.utils.messages import (
    ConfigurationMessage,
    DistributionMessage, SusceptibilityGroupMessages
)
from src.utils.response import UJSONResponse

susceptibility_groups_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Susceptibility Groups"]
)


@susceptibility_groups_routes.post("/susceptibility_group")
def create_susceptibility_group(
    conf_uuid: UUID,
    susceptibility_group: NewSusceptibilityGroup,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create susceptibility group from specific object.

    \f
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


@susceptibility_groups_routes.put("/susceptibility_group/{uuid}")
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
        sg_found.update(**susceptibility_group.dict(exclude=None))
        sg_found.reload()

        return UJSONResponse(
            SusceptibilityGroupMessages.updated,
            HTTP_200_OK,
            BsonObject.dict(sg_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@susceptibility_groups_routes.get("/susceptibility_group/{uuid}")
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


@susceptibility_groups_routes.get("/susceptibility_group")
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

        sg_found = SusceptibilityGroupInterface.find_by_conf(
            configuration
        )

        return UJSONResponse(
            SusceptibilityGroupMessages.found,
            HTTP_200_OK,
            BsonObject.dict(sg_found)
        )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@susceptibility_groups_routes.delete("/susceptibility_group/{uuid}")
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


@susceptibility_groups_routes.put("/susceptibility_group/{uuid}/file")
def update_distribution_file(
    conf_uuid: UUID,
    uuid: UUID,
    file: UploadFile = File(...),
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

        is_valid = VerifySimpleDistributionFile.handle(
            file,
            sg_found
        )
        if not is_valid:
            return UJSONResponse(
                DistributionMessage.invalid,
                HTTP_400_BAD_REQUEST
            )

        data, is_invalid = SaveDistributionFile.handle(
            file,
            configuration,
            sg_found.name
        )
        if is_invalid:
            return UJSONResponse(
                DistributionMessage.can_not_save,
                HTTP_400_BAD_REQUEST
            )
        sg_found.distribution.file_id = data.get('id')
        sg_found.save().reload()

        return UJSONResponse(
            DistributionMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(sg_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)