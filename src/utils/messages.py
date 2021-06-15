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
    deleted: str = "Configuration has been deleted"
    found: str = "Configuration found"
    not_found: str = "Configuration not found"
    exist: str = "Configuration exist"
    created: str = "Configuration has been created"
    updated: str = "Configuration updated"


@dataclass
class MobilityGroupsMessages:
    """
    Messages used in endpoint responses for mobility groups
    """
    found: str = "Mobility Groups found"
    not_found: str = "Mobility Groups not found"
    exist: str = 'Mobility Groups exist'
    created: str = "Mobility Groups has been created"
    updated: str = "Mobility Groups updated"
    not_mobility_group_entered: str = "Mobility Groups not entered"
    not_distribution_entered: str = "Distribution not entered"


@dataclass
class QuarantineGroupsMessages:
    """
    Messages used in endpoint responses for quarantine groups
    """
    found: str = "Quarantine Groups found"
    not_found: str = "Quarantine Groups not found"
    exist: str = 'Quarantine Groups exist'
    created: str = "Quarantine Groups has been created"
    updated: str = "Quarantine Groups updated"
    not_quarantine_groups_entry: str = "Quarantine Groups not entry"


@dataclass
class AgeGroupsMessages:
    """
    Messages used in endpoint responses for age groups
    """
    found: str = "Age groups found"
    not_found: str = "Age groups not found"
    not_age_groups_entered: str = "Not age groups entered to save"
    created: str = "Age groups has been created"
    updated: str = "Age groups updated"
    deleted: str = "Age group deleted"
    bad_deleted: str = "Age group bad deleted"


@dataclass
class SecurityMessage:
    invalid_token: str = "Invalid Token"


@dataclass
class NaturalHistoryMessage:
    """
    Messages used in endpoint responses for natural history
    """
    found: str = "Natural history found"
    not_found: str = "Natural history not found"
    exist: str = "Natural history exist"
    created: str = "Natural history has been created"
    updated: str = "Natural history updated"


class SusceptibilityGroupsMessages:
    """
    Messages used in endpoint responses for susceptibility groups
    """
    found: str = "Susceptibility groups found"
    not_found: str = "Susceptibility groups not found"
    exist: str = 'Susceptibility groups exist'
    created: str = "Susceptibility groups has been created"
    updated: str = "Susceptibility groups updated"
    not_susceptibility_group_entered = "Susceptibility groups not entered"


@dataclass
class ImmunizationGroupMessage:
    exist: str = "Immunization group exist"
    found: str = "Age groups found"
    not_found: str = "Age groups not found"
    not_age_immunization_entered: str = "Not immunization groups entered to save"
    created: str = "Age groups has been created"
    updated: str = "Age groups updated"
    deleted: str = "Age group deleted"
    bad_deleted: str = "Age group bad deleted"


@dataclass
class VulnerabilityGroupMessage:
    exist: str = "Vulnerability group exist"
    found: str = "Vulnerability Groups found"
    not_found: str = "Vulnerability Groups not found"
    not_vulnerability_entered: str = "Not Vulnerability Groups entered to save"
    created: str = "Vulnerability Groups has been created"
    updated: str = "Vulnerability Groups updated"
    deleted: str = "Vulnerability Groups deleted"
    bad_deleted: str = "Vulnerability Groups bad deleted"


@dataclass
class DiseaseGroupMessage:
    found: str = "Disease groups found"
    not_found: str = "Disease groups not found"
    exist: str = "Disease Groups exist"
    created: str = "Disease Groups has been created"
    not_entered: str = "Disease Groups not entered to save"
