class Units:

    units_length = {
        "km": "kilometers",
        "m":"meters",
        "cm":"centimeters",
        "ft": "feet",
        "mi": "international mile",
        "yd": "international yard"
    }
    
    units_time = {
        "min": "minutes",
        "h": "hours",
        "d": "days"
    }


    @classmethod
    def distance(cls):
        """
        Get distance units
        """
        return cls.units_length

    @classmethod
    def time(cls):
        """
        Get time units
        """
        return cls.units_time
