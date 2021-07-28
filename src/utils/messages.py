from dataclasses import dataclass


@dataclass
class UnitsMessage:
    """
    Messages used in endpoint responses for units 
    """
    tracing: str = "Quarantine tracing variables"
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
    invalid: str = "Invalid distribution file"
    valid: str = "Valid distribution file"
    updated: str = "Updated distribution file"
    can_not_save: str = "Can not save distribution file"


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
    found: str = "Mobility group found"
    not_found: str = "Mobility group not found"
    exist: str = "Mobility group exist"
    created: str = "Mobility group has been created"
    updated: str = "Mobility group updated"
    deleted: str = "Mobility group deleted"


class SusceptibilityGroupMessages:
    """
    Messages used in endpoint responses for susceptibility groups
    """
    deleted: str = "Susceptibility group has been deleted"
    found: str = "Susceptibility group found"
    not_found: str = "Susceptibility group not found"
    exist: str = "Susceptibility group exist"
    created: str = "Susceptibility group has been created"
    updated: str = "Susceptibility group updated"


@dataclass
class QuarantineMessage:
    found: str = "Quarantine found"
    not_found: str = "Quarantine not found"
    updated: str = "Quarantine updated"


@dataclass
class QuarantineGroupMessages:
    """
    Messages used in endpoint responses for quarantine groups
    """
    found: str = "Quarantine Groups found"
    not_found: str = "Quarantine Groups not found"
    exist: str = "Quarantine Groups exist"
    created: str = "Quarantine Groups has been created"
    updated: str = "Quarantine Groups updated"
    not_quarantine_groups_entered: str = "Quarantine Groups not entered"
    quarantine_restriction_not_found: str = "Quarantine restrictions not found"
    quarantine_restriction_found: str = "Quarantine restrictions found"


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
    invalid_distribution: str = "Natural history distribution not config"
    invalid_transition: str = "Natural history transition not config"


@dataclass
class ImmunizationGroupMessage:
    exist: str = "Immunization group exist"
    found: str = "Immunization group found"
    not_found: str = "Immunization group not found"
    not_entered: str = "Immunization groups not entered to save"
    created: str = "Immunization group has been created"
    updated: str = "Immunization group updated"
    deleted: str = "Immunization group deleted"
    bad_deleted: str = "Immunization group bad deleted"


@dataclass
class VulnerabilityGroupMessage:
    exist: str = "Vulnerability group exist"
    found: str = "Vulnerability groups found"
    not_found: str = "Vulnerability groups not found"
    not_entered: str = "Vulnerability groups not entered to save"
    created: str = "Vulnerability groups has been created"
    updated: str = "Vulnerability groups updated"
    deleted: str = "Vulnerability groups deleted"
    bad_deleted: str = "Vulnerability groups bad deleted"


@dataclass
class DiseaseGroupMessage:
    found: str = "Disease groups found"
    not_found: str = "Disease groups not found"
    exist: str = "Disease groups exist"
    created: str = "Disease groups has been created"
    updated: str = "Disease groups has been updated"
    deleted: str = "Disease groups has been deleted"
    not_entered: str = "Disease groups not entered to save"
    missing_conf: str = "Disease group distribution is empty"
    invalid_distribution: str = "Disease group distribution not config"


@dataclass
class PopulationMessage:
    not_found: str = "Population configuration not found"
    found: str = "Population variables found"
    updated: str = "Population updated"
