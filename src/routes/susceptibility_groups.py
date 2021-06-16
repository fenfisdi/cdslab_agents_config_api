from fastapi import APIRouter
from starlette.status import HTTP_200_OK, \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND

from src.interfaces import \
    SusceptibilityGroupInterface, DistributionInterface
from src.models import SusceptibilityGroup, \
    NewSusceptibilityGroup, Distribution, NewDistribution
from src.utils.messages import SusceptibilityGroupsMessages
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


susceptibility_groups_routes = \
    APIRouter(tags=["SusceptibilityGroups"])


@susceptibility_groups_routes.get("/susceptibility_groups")
def find_all():
    """
    Get all existing susceptibility groups in db
    """
    try:
        susceptibility_groups = \
            SusceptibilityGroupInterface.find_all()
        if not susceptibility_groups:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(susceptibility_groups)
    )


@susceptibility_groups_routes.get(
    "/susceptibility_groups/{configuration_identifier}"
)
def find_by_configuration(
        configuration_identifier: str
):
    """
    Get existing susceptibility groups by configuration identifier

    \f
    :param configuration_identifier: Configuration identifier
    """
    try:
        mobility_groups = SusceptibilityGroupInterface. \
            find_by_configuration(configuration_identifier)
        if not mobility_groups:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_found,
                HTTP_404_NOT_FOUND
            )
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.found,
        HTTP_200_OK,
        BsonObject.dict(mobility_groups)
    )


@susceptibility_groups_routes.post(
    "/susceptibility_groups/{configuration_identifier}"
)
def create_mobility_group(
        configuration_identifier: str,
        mobility_group: NewSusceptibilityGroup,
        distribution: NewDistribution
):
    try:
        if not mobility_group:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_mobility_group_entry,
                HTTP_400_BAD_REQUEST
            )

        if not distribution:
            return UJSONResponse(
                SusceptibilityGroupsMessages.not_distribution_entry,
                HTTP_400_BAD_REQUEST
            )

        mobility_groups_found = SusceptibilityGroupInterface. \
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

        mobility_group = SusceptibilityGroup(**mobility_group)
        mobility_group.save()
    except Exception as error:
        return UJSONResponse(
            str(error),
            HTTP_400_BAD_REQUEST
        )

    return UJSONResponse(
        SusceptibilityGroupsMessages.created,
        HTTP_201_CREATED,
        BsonObject.dict(mobility_group)
    )
