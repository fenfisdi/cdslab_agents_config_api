from typing import List, Set
from uuid import uuid1

from src.interfaces import (
    AgeGroupInterface,
    DiseaseGroupInterface,
    MobilityGroupInterface,
    PopulationInterface,
    QuarantineGroupInterface,
    SusceptibilityGroupInterface,
    VulnerabilityGroupInterface
)
from src.models.db import Configuration, Population
from src.models.general import Groups
from src.models.route_models import UpdateVariable
from src.utils import BsonObject


class ValidatePopulationDefault:

    @classmethod
    def handle(cls, configuration: Configuration) -> None:
        """
        Validate if exist a population in a configuration, if it didn't exist it
        will create a population for a configuration.

        :param configuration: Configuration associated to the population.
        """
        population = PopulationInterface.find_one_by_conf(configuration)
        if not population:
            population = Population(
                identifier=uuid1(),
                configuration=configuration,
                allowed_configuration={Groups.AGE.value},
                allowed_variables={
                    unit.value for unit in Groups if
                    unit != Groups.AGE
                }
            )
        population.save()


class FindAllowedVariables:

    @classmethod
    def handle(cls, population: Population, variable: Set[Groups]) -> List:
        """
        Find all allowed variables to update in a population and return its
        values.

        :param population:
        :param variable:
        """
        current_values = population.values
        values = [
            unit.value for unit in Groups
            if unit.value in current_values.keys()
        ]
        # Add default value to the list
        values.insert(0, Groups.AGE.value)

        if not variable:
            variable = {}
        allowed_variables = []
        for i in values:
            if Groups(i) not in variable:
                allowed_variables.append(i)
        return allowed_variables


class UpdatePopulationValues:

    @classmethod
    def handle(cls, population: Population, variables: UpdateVariable):
        """
        Update population variable according to variable input.

        :param population: Population specification to update information.
        :param variables: Input information to update.
        """
        variables_dict = variables.dict()
        current_values = population.values
        current_values.update(
            {variables_dict.get("variable"): variables_dict.get("values")}
        )

        allowed_configuration = population.allowed_configuration
        allowed_configuration.append(variables.variable)

        allowed_variables = population.allowed_variables
        if variables.variable in allowed_variables:
            allowed_variables.remove(variables.variable)

        population.update(
            values=current_values,
            allowed_configuration=allowed_configuration,
            allowed_variables=allowed_variables
        )
        population.reload()


class DeletePopulationValues:

    @classmethod
    def handle(cls, population: Population, variable: Groups):
        """
        Delete population values from specific configuration and delete its
        chain

        :param population: population to modify values.
        :param variable: variable to delete information in the values.
        """
        population_values = population.values
        if variable.value in population_values.keys():
            del population_values[variable.value]

        population.update(values=population_values)


class FindVariableResults:

    @classmethod
    def handle(cls, configuration: Configuration, variable: Groups) -> dict:
        """
        Find specific configuration from simulation according to specific
        variable, return all data from each interface.

        :param configuration: configuration associated to find variable in the
        interface
        :param variable: type of variable to find
        """
        interface_dict = {
            Groups.AGE: AgeGroupInterface,
            Groups.MOBILITY: MobilityGroupInterface,
            Groups.SUSCEPTIBILITY: SusceptibilityGroupInterface,
            Groups.VULNERABILITY: VulnerabilityGroupInterface,
            Groups.DISEASE: DiseaseGroupInterface,
            Groups.QUARANTINE: QuarantineGroupInterface,
        }
        interface = interface_dict.get(variable)
        if interface:
            return BsonObject.dict(interface.find_all_by_conf(configuration))
        return dict()


class FindVariablesConfigured:

    @classmethod
    def handle(cls, population: Population) -> list:
        """
        Find all variables configured in population configuration, except age
        configuration and return an array variables.

        :param population: population configuration to find variables.
        """
        variables_configured = list(set(population.allowed_configuration))
        variables_configured.remove("age")
        return variables_configured
