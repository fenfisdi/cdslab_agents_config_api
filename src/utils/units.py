class Units:

    #TODO:

    units_length = {"Km": "Kilometres",
            "M":"Meter",
            "c":"Centimeter"}

    @classmethod
    def distance(cls):
        '''
            Get units distance
        Return:
            List: Distance units list
        '''
        return cls.units_length