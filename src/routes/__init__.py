from .age_groups import age_group_routes
from .configuration import configuration_routes
from .disease_states import disease_states_routes
from .distributions import distributions_routes
from .immunization_groups import immunization_routes
from .mobility_groups import mobility_group_routes
from .natural_history import natural_history_routes
from .susceptibility_groups import susceptibility_groups_routes
from .units import units_routes
from .vulnerability_groups import vulnerability_group_routes

__all__ = [
    "units_routes",
    "distributions_routes",
    "disease_states_routes",
    "configuration_routes",
    "mobility_group_routes",
    "age_group_routes",
    "natural_history_routes",
    "age_group_routes",
    "susceptibility_groups_routes",
    "immunization_routes",
    "vulnerability_group_routes"
]
