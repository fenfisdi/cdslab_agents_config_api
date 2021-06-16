from src.models.db.master.distribution import MasterDistribution


class DistributionInterface:
    """
        Interface to consult distributions in DB
    """

    @staticmethod
    def find_all():
        """
        Find all distributions in DB
        """
        return MasterDistribution.objects().only("name").all()

    @staticmethod
    def find_parameters(name: str):
        """
        Search for distributions that match the name

        :param name: distribution name
        """
        filters = dict(
            name=name
        )
        return MasterDistribution.objects(
            **filters
        ).first()
