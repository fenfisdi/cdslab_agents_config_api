from dataclasses import dataclass


@dataclass
class UnitsMessage:
    """
    Messages used in endpoint responses for units 
    """
    distance: str = "Units distance"
    time: str = "Time units"
    distance_not_found = "Distance units not found"
    time_not_found: str = "Time units not found"


@dataclass
class DistributionMessage:
    """
    Messages used in endpoint responses for distributions
    """
    found: str = "Found distributions"
    not_found: str = "Distributions not found"
    not_exist: str = "Distribution does not exist"
    disease_states_distribution_found = "Found disease states distribution"


@dataclass
class DiseaseStatesMessage:
    """
    Messages used in endpoint responses for distributions
    """
    found: str = "Found states"
    not_found: str = "States not found"


@dataclass
class ConfigurationMessage:
    """
    Messages used in endpoint responses for configuration
    """
    found: str = "Configuration found"
    not_found: str = "Configuration not found"
    exist: str = 'Configuration exist'
    created: str = "Configuration has been created"
    updated: str = "Configuration updated"


@dataclass
class AgeGroupsMessages:
    """
    Messages used in endpoint responses for age groups
    """
    found: str = "Age groups found"
    not_found: str = "Age groups not found",
    not_age_groups_entry: str = "Not age groups entry to save",
    created: str = "Age groups has been created"
    updated: str = "Age groups updated"
    deleted: str = "Age group deleted"
    bad_deleted: str = "Age group bad deleted"
