from typing import Set
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from src.interfaces import ConfigurationInterface, PopulationInterface
from src.models.general import Groups
from src.models.route_models import UpdateVariable
from src.use_case import (
    DeletePopulationValues,
    FindAllowedVariables,
    FindVariableResults,
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

    :param conf_uuid: Configuration identifier.
    :param variable_information:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

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

    :param conf_uuid: Configuration identifier.
    :param variable:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    ValidatePopulationDefault.handle(conf_found)
    population = PopulationInterface.find_one_by_conf(conf_found)

    DeletePopulationValues.handle(population, variable)


@population_routes.get("/population/group")
def list_allowed_groups(
    conf_uuid: UUID,
    variable: Set[Groups] = Query(None),
    user = Depends(SecurityUseCase.validate)
):
    """
    List all allowed groups to configuration.

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

    :param conf_uuid: Configuration identifier.
    :param variable:
    :param user: User authenticated.
    """
    conf_found = ConfigurationInterface.find_one_by_id(conf_uuid, user)
    if not conf_found:
        return UJSONResponse(ConfigurationMessage.not_found, HTTP_404_NOT_FOUND)

    values = FindVariableResults.handle(conf_found, variable)
    return UJSONResponse(PopulationMessage.values_found, HTTP_200_OK, values)
