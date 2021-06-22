from .units import units_routes
from .distributions import distributions_routes
from .disease_states import disease_states_routes
from .mobility_groups import mobility_group_routes
from .configuration import configuration_routes
from .age_groups import age_group_routes
from .natural_history import natural_history_routes
from .intial_population import initial_population_routes

__all__ = [
    "units_routes",
    "distributions_routes",
    "disease_states_routes",
    "configuration_routes",
    "mobility_group_routes",
    "age_group_routes",
    "natural_history_routes",
    "initial_population_routes"
]
