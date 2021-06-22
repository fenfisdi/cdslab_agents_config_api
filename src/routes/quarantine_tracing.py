from uuid import UUID, uuid1

from fastapi import APIRouter
from typing import List
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from src.interfaces import (
    QuarantineTracingInterface,
    ConfigurationInterface,
    QuarantineGroupInterface
)

from src.models import (
    NewQuarantineTracing,
    QuarantineTracing
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse
from src.utils.messages import (
    ConfigurationMessage,
    QuarantineTracingMessage
)


quarantine_tracing_routes = APIRouter(tags=["QuarantineTracing"])


@quarantine_tracing_routes.get("/quarantine_tracing/{conf}")
def find_by_conf(conf: UUID):
    """
    Find all quarantine tracing by configuration

    \f
    :param conf: Configuration Identifier
    """
    try:
        conf_found = ConfigurationInterface.find_by_identifier(
            conf
        )

        if not conf_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        quarantine_tracing = QuarantineTracingInterface.find_by_conf(
            conf_found
        )
        if not quarantine_tracing:
            return UJSONResponse(
                QuarantineTracingMessage.not_found
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineTracingMessage.foud,
        HTTP_200_OK,
        BsonObject.dict(quarantine_tracing)
    )


@quarantine_tracing_routes.post("/")
def create_quarantine_tracing(
        conf: UUID,
        quarantine_tracing: NewQuarantineTracing
):
    try:
        if not quarantine_tracing:
            return UJSONResponse(
                QuarantineTracingMessage.quarantine_tracing_not_entered,
                HTTP_400_BAD_REQUEST
            )

        conf_found = ConfigurationInterface.find_by_identifier(
            conf
        )

        if not conf_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        new_quarantine_tracing = QuarantineTracing(
            identifier=uuid1(),
            configuration=conf_found,
            **quarantine_tracing
        )
        new_quarantine_tracing.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineTracingMessage.created,
        HTTP_201_CREATED
    )
