class Units:

    #TODO:

    units_length = {"km": "kilometers",
            "m":"meters",
            "cm":"centimeters",
            "ft": "feet",
            "mi": "international mile",
            "yd": "international yard"}

    @classmethod
    def distance(cls):
        '''
            Get units distance
        Return:
            List: Distance units list
        '''
        return cls.units_length
