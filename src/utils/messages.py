from dataclasses import dataclass


@dataclass
class UnitsMessage:
    '''
        Messages used in endpoint responses for units 
    '''
    distance: str = "Units distance"
    time: str = "Time units"


@dataclass
class DistributionMessage:
    '''
        Messages used in endpoint responses for distributions
    '''
    found: str = 'Found distributions'
    not_found: str = 'Distributions not found'
    not_exist: str = 'Distribution does not exist'
    
@dataclass
class DiseaseStatesMessage:
    """
        Messages used in endpoint responses for distributions
    """
    found: str = 'Found states'
    not_found: str = 'States not found'
