from dataclasses import dataclass


@dataclass
class UnitsMessage:
    """
        Messages used in endpoint responses for units 
    """
    distance: str = "Units distance"
    time: str = "Time units"


@dataclass
class DistributionMessage:
    """
        Messages used in endpoint responses for distributions
    """
    found: str = 'Found distributions'
    not_found: str = 'Distributions not found'
    not_exist: str = 'Distribution does not exist'
    disease_states_distribution_found = 'Found disease states distribution'
