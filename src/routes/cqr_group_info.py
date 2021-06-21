from uuid import UUID, uuid1

from fastapi import APIRouter
from typing import List
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    CQRGroupInfoInterface,
    ConfigurationInterface,
    QuarantineGroupInterface
)

from src.models import (
    NewCQRGroupInfo,
    CQRGroupInfo,
    NewCyclicQuarantineRestriction,
    CyclicQuarantineRestriction
)
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse
from src.utils.messages import (
    ConfigurationMessage,
    QuarantineGroupsMessages,
    CQRGroupInfoMessages
)


cqr_group_info_routes = APIRouter(tags=["CQRGroupInfo"])


@cqr_group_info_routes.get("/cqr_group_info/{configuration}")
def find_by_configuration_quarantine(
        configuration: UUID
):
    """
    Find all CQRGroupInfo by configuration and quarantine group in db

    \f
    :param configuration: Configuration identifier
    """
    try:
        configuration_found = ConfigurationInterface.find_by_identifier(
            configuration
        )

        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        cqr_group_info = CQRGroupInfoInterface.find_by_configuration(
            configuration
        )

        if not cqr_group_info:
            return UJSONResponse(
                CQRGroupInfoMessages.not_found,
                HTTP_404_NOT_FOUND
            )

    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        QuarantineGroupsMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(cqr_group_info)
    )


@cqr_group_info_routes.post("/cqr_group_info/{configuration}")
def create_cqr_group_info(
        configuration: UUID,
        cqr_groups_info: List[NewCQRGroupInfo],
        cyclic_quarantine_restriction: NewCyclicQuarantineRestriction
):
    """
    Create a CQRGroupInfo in db

    \f
    :param configuration: Configuration identifier
    :param cqr_groups_info: List of CQRGroupInfo to insert in db
    :param cyclic_quarantine_restriction: CyclicQuarantineRestriction to insert in db
    """
    try:
        if not cqr_groups_info:
            return UJSONResponse(
                CQRGroupInfoMessages.cqr_group_not_entered,
                HTTP_404_NOT_FOUND
            )

        configuration_found = ConfigurationInterface.find_by_identifier(
            configuration
        )

        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        cqr_groups_info_found = CQRGroupInfoInterface.find_by_configuration(
            configuration_found
        )

        if cqr_groups_info_found:
            for cqr_group_info in cqr_groups_info_found:
                cqr_group_info.delete()

        for cqr_group_info in cqr_groups_info:
            aux_cqr_group_info = cqr_group_info.dict()
            print(aux_cqr_group_info["quarantine_identifier"])
            quarantine = QuarantineGroupInterface.find_by_identifier(
                aux_cqr_group_info["quarantine_identifier"]
            )
            del aux_cqr_group_info["quarantine_identifier"]
            print(quarantine)
            new_cqr_group_info = CQRGroupInfo(
                identifier=uuid1(),
                configuration=configuration_found,
                quarantine_group=quarantine,
                **aux_cqr_group_info
            )
            new_cqr_group_info.save()

        new_cyclic_quarantine_restriction = CyclicQuarantineRestriction(
            identifier=uuid1(),
            configuration=configuration_found,
            **cyclic_quarantine_restriction.dict()
        )
        new_cyclic_quarantine_restriction.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        CQRGroupInfoMessages.created,
        HTTP_201_CREATED
    )


