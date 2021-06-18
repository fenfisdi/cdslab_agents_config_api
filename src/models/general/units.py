from enum import Enum


class UnitLength(Enum):
    KM: str = 'kilometers'
    M: str = 'meters'
    CM: str = 'centimeters'
    FT: str = 'feet'
    MI: str = 'international miles'
    YD: str = 'international yards'


class UnitTime(Enum):
    MIN: str = 'minutes'
    H: str = 'hours'
    D: str = 'days'
