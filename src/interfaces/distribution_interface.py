from src.models.db.distribution import Distribution

class DistributionInterface:
    '''
        Interface to consult distributions in DB
    '''

    @staticmethod
    def find_all():
        '''
            Find all distributions in BD
        Returns:
            Names Distributions in BD
        '''
        return Distribution.objects().only("name").all()

    @staticmethod
    def find_parameters(name: str):
        '''
            Search for distributions that match the name
        Parameter:
            name (str): distribution name
        Returns:
            Distribution name and parameters
        '''
        filters = dict(
            name=name
        )
        return Distribution.objects(
            **filters
        ).first()
