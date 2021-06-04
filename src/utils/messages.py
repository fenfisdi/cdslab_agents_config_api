from dataclasses import dataclass

@dataclass
class UnitsMessage:
    '''
        Messages used in endpoint responses for units 
    '''
    distance: str = "Units distance"