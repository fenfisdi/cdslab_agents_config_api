from typing import Set
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ConfigurationInterface, PopulationInterface
from src.models.general import Groups
from src.models.route_models import UpdateVariable
from src.use_case import (
    DeletePopulationValues,
    FindAllowedVariables,
    FindPopulationData,
    FindVariableResults,
    FindVariablesConfigured,
    SecurityUseCase,
    UpdatePopulationValues,
    ValidatePopulationDefault
)
from src.utils.messages import ConfigurationMessage, PopulationMessage
from src.utils.response import UJSONResponse

population_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Population"]
)


@population_routes.get("/population/variables")
def list_allowed_variables(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    List allowed variables to config inside population configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)

    population = PopulationInterface.find_one_by_conf(conf_found)
    if not population:
        return UJSONResponse(PopulationMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(
        PopulationMessage.found,
        HTTP_200_OK,
        population.allowed_variables
    )


@population_routes.put("/population")
def create_population_configuration(
    conf_uuid: UUID,
    variable_information: UpdateVariable,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create specific configuration inside population according to a variable.

    \f
    :param conf_uuid: Configuration identifier.
    :param variable_information:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)

    population = PopulationInterface.find_one_by_conf(conf_found)

    UpdatePopulationValues.handle(population, variable_information)

    return UJSONResponse(
        PopulationMessage.updated,
        HTTP_200_OK,
        population.values
    )


@population_routes.delete("/population")
def delete_population_configuration(
    conf_uuid: UUID,
    variable: Groups = Query(...),
    user = Depends(SecurityUseCase.validate)
):
    """
    Delete specific group in each configuration population.

    \f
    :param conf_uuid: Configuration identifier.
    :param variable:
    :param user: User authenticated.
    """
    if variable.value is variable.AGE.value:
        return UJSONResponse(
            PopulationMessage.age_exception,
            HTTP_400_BAD_REQUEST
        )
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)
    population = PopulationInterface.find_one_by_conf(conf_found)

    is_deleted = DeletePopulationValues.handle(population, variable)
    if not is_deleted:
        return UJSONResponse(PopulationMessage.not_deleted, HTTP_400_BAD_REQUEST)

    return UJSONResponse(PopulationMessage.deleted, HTTP_200_OK)


@population_routes.get("/population/group")
def list_allowed_groups(
    conf_uuid: UUID,
    variable: Set[Groups] = Query(None),
    user = Depends(SecurityUseCase.validate)
):
    """
    List all allowed groups to configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param variable:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)
    population = PopulationInterface.find_one_by_conf(conf_found)
    if not population:
        return UJSONResponse(PopulationMessage.not_found, HTTP_404_NOT_FOUND)

    value = FindAllowedVariables.handle(population, variable)

    return UJSONResponse(PopulationMessage.found, HTTP_200_OK, value)


@population_routes.get("/population/value")
def list_allowed_values(
    conf_uuid: UUID,
    variable: Groups = Query(...),
    user = Depends(SecurityUseCase.validate)
):
    """
    List all allowed values for each group.

    \f
    :param conf_uuid: Configuration identifier.
    :param variable:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    values = FindVariableResults.handle(conf_found, variable)
    return UJSONResponse(PopulationMessage.values_found, HTTP_200_OK, values)


@population_routes.get("/population/configured")
def list_groups_configured(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    List all groups configured in population.

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)

    population = PopulationInterface.find_one_by_conf(conf_found)
    if not population:
        return UJSONResponse(PopulationMessage.not_found, HTTP_404_NOT_FOUND)

    try:
        data = FindVariablesConfigured.handle(population)
        return UJSONResponse(PopulationMessage.values_found, HTTP_200_OK, data)
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@population_routes.get("/population/saved")
def find_saved_values(
    conf_uuid: UUID,
    variable: Groups = Query(...),
    user = Depends(SecurityUseCase.validate)
):
    """
    Find current values in a specific population according to the variable
    configured.

    \f
    :param conf_uuid: Configuration identifier.
    :param variable: Variable configured to find information.
    :param user: User authenticated by token.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    population = PopulationInterface.find_one_by_conf(conf_found)
    if not population:
        return UJSONResponse(PopulationMessage.not_found, HTTP_404_NOT_FOUND)

    try:
        data = FindPopulationData.handle(population, variable)
        return UJSONResponse(PopulationMessage.values_found, HTTP_200_OK, data)
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
