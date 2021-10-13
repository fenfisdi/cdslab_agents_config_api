from uuid import UUID, uuid1

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ConfigurationInterface
from src.models.db import Configuration
from src.models.route_models import NewConfiguration, UpdateConfiguration
from src.services import FileAPI
from src.use_case import FindAgentInformation, SecurityUseCase
from src.utils.encoder import BsonObject
from src.utils.messages import ConfigurationMessage
from src.utils.response import UJSONResponse

configuration_routes = APIRouter(tags=["Configuration"])


@configuration_routes.get("/configuration")
def list_configurations(user = Depends(SecurityUseCase.validate)):
    """
    Get all existing configurations in db.

    \f
    :param user: User authenticated by token.
    """
    try:
        configuration = ConfigurationInterface.find_all(user)

        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.found,
        HTTP_200_OK,
        BsonObject.dict(configuration)
    )


@configuration_routes.get("/configuration/{uuid}")
def find_configuration(uuid: UUID, user = Depends(SecurityUseCase.validate)):
    """
    Find simulation configuration by its uuid.

    \f
    :param uuid: Identifier of simulation.
    :param user: User authenticated by token.
    """
    configuration_found = ConfigurationInterface.find_one_by_id(uuid, user)
    if not configuration_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        ConfigurationMessage.found,
        HTTP_200_OK,
        BsonObject.dict(configuration_found)
    )


@configuration_routes.post("/configuration")
def create_configuration(
    configuration: NewConfiguration,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create a new configuration in db.

    \f
    :param configuration: Configuration object to insert in db.
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_name(
            configuration.name,
            user
        )
        if configuration_found:
            return UJSONResponse(
                ConfigurationMessage.exist,
                HTTP_400_BAD_REQUEST
            )

        new_configuration = Configuration(
            **configuration.dict(),
            identifier=uuid1(),
            user=user
        )
        new_configuration.save()

        response, is_invalid = FileAPI.create_simulation_folder(
            user.email,
            new_configuration.identifier
        )
        if is_invalid:
            return response

        return UJSONResponse(
            ConfigurationMessage.created,
            HTTP_201_CREATED,
            BsonObject.dict(new_configuration)
        )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )


@configuration_routes.put("/configuration/{uuid}")
def updated_configuration(
    uuid: UUID,
    configuration: UpdateConfiguration,
    user = Depends(SecurityUseCase.validate)
):
    """
    Update a configuration in db.

    \f
    :param uuid: Identifier of simulation.
    :param configuration: Configuration object to insert in db
    :param user: User authenticated by token.
    """
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        configuration_found.update(**configuration.dict(exclude_none=True))
        configuration_found.save().reload()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.updated,
        HTTP_200_OK,
        BsonObject.dict(configuration_found)
    )


@configuration_routes.delete("/configuration/{uuid}")
def delete_configuration(
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete simulation.

    \f
    :param uuid: Identifier of simulation.
    :param user: User authenticated by token.
    """
    configuration_found = ConfigurationInterface.find_one_by_id(uuid, user)
    if not configuration_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    try:
        configuration_found.update(is_deleted=True)
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(ConfigurationMessage.deleted, HTTP_200_OK)


@configuration_routes.get("/configuration/{uuid}/summary")
def get_summary_configuration(
    uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find all configuration simulation and all its data.

    \f
    :param uuid:
    :param user:
    """
    configuration_found = ConfigurationInterface.find_one_by_id(uuid, user)
    if not configuration_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    simulation_data = FindAgentInformation.handle(configuration_found)

    return UJSONResponse(
        ConfigurationMessage.found,
        HTTP_200_OK,
        simulation_data
    )
