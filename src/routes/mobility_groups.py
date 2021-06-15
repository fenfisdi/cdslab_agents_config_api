from fastapi import APIRouter
from starlette.status import HTTP_200_OK, \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND

from src.interfaces import MobilityGroupInterface, \
    DistributionInterface
from src.models import MobilityGroup, Distribution, \
    NewMobilityGroup, NewDistribution
from src.utils.messages import MobilityGroupsMessages
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


mobility_group_routes = APIRouter(tags=["MobilityGroups"])


@mobility_group_routes.get("/mobility_groups")
def find_all():
    """
    Get all existing mobility group in db
    """
    try:
        mobility_groups = MobilityGroupInterface.find_all()
        if not mobility_groups:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(mobility_groups)
    )


@mobility_group_routes.get(
    "/mobility_groups/{configuration_identifier}"
)
def find_by_configuration(
        configuration_identifier: str
):
    """
    Get existing mobility groups by configuration identifier

    \f
    :param configuration_identifier: Configuration identifier
    """
    try:
        mobility_groups = MobilityGroupInterface. \
            find_by_configuration(configuration_identifier)
        if not mobility_groups:
            return UJSONResponse(
                MobilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(mobility_groups)
    )


@mobility_group_routes.post(
    "/mobility_groups/{configuration_identifier}"
)
def create_mobility_group(
        configuration_identifier: str,
        mobility_group: NewMobilityGroup,
        distribution: NewDistribution
):
    try:
        if not mobility_group:
            return UJSONResponse(
                MobilityGroupsMessages.not_mobility_group_entry,
                HTTP_400_BAD_REQUEST
            )

        if not distribution:
            return UJSONResponse(
                MobilityGroupsMessages.not_distribution_entry,
                HTTP_400_BAD_REQUEST
            )

        mobility_groups_found = MobilityGroupInterface. \
            find_by_configuration(configuration_identifier)
        if mobility_groups_found:
            for mobility_group in mobility_groups_found:
                distribution_found = DistributionInterface. \
                    find_one(mobility_group.distribution)
                if distribution_found:
                    distribution.delete()
                mobility_group.delete()

        new_distribution = Distribution(**distribution)
        new_distribution.save()

        mobility_group = MobilityGroup(**mobility_group)
        mobility_group.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        MobilityGroupsMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(mobility_group)
    )
