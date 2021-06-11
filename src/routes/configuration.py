from fastapi import APIRouter
from starlette.status import HTTP_200_OK, \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND

from src.interfaces import ConfigurationInterface
from src.models import Configuration, NewConfiguration
from src.utils.messages import ConfigurationMessage
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


configuration_routes = APIRouter(tags=["Configuration"])


@configuration_routes.get("/configuration")
def find_all():
    """
    Get all existing configurations in db
    """
    try:
        configuration = ConfigurationInterface.find_all()

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


@configuration_routes.post("/configuration")
def create_configuration(configuration: NewConfiguration):
    """
    Create a new configuration in db

    \f
    :param configuration: Configuration object to insert in bd
    """
    try:
        configuration_found = ConfigurationInterface.find_by_name(configuration.name)
        if configuration_found:
            return UJSONResponse(
                ConfigurationMessage.exist,
                HTTP_400_BAD_REQUEST
            )

        new_configuration = Configuration(**configuration)
        new_configuration.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        ConfigurationMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_configuration)
    )


@configuration_routes.put("/configuration")
def updated_configuration(configuration: NewConfiguration):
    """
    Update a configuration in db

    \f
    :param configuration: Configuration object to insert in bd
    """
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(configuration.identifier)
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
