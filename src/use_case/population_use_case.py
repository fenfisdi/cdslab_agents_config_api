from typing import List, Set
from uuid import uuid1

from src.interfaces import PopulationInterface
from src.models.db import Configuration, Population
from src.models.general import Groups
from src.models.route_models import UpdateVariable


class ValidatePopulationDefault:

    @classmethod
    def handle(cls, configuration: Configuration):
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
        current_values = population.values
        values = [
            unit.value for unit in Groups
            if unit.value in current_values.keys()
        ]
        values.insert(0, Groups.AGE.value)
        for i in variable:
            values.remove(i)
        return values


class UpdatePopulationValues:

    @classmethod
    def handle(cls, population: Population, variables: UpdateVariable):
        variables_dict = variables.dict()
        current_values = population.values
        current_values.update(
            {variables_dict.get("variable"): variables_dict.get("values")}
        )

        allowed_configuration = population.allowed_configuration
        allowed_configuration.append(variables.variable)

        allowed_variables = population.allowed_variables
        allowed_variables.remove(variables.variable)

        population.update(
            values=current_values,
            allowed_configuration=allowed_configuration,
            allowed_variables=allowed_variables
        )
        population.reload()
