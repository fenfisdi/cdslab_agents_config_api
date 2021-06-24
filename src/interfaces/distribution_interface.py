from src.models.db.distribution import Distribution
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
    def find_one(identifier: str):
        """
        Find a distribution in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return Distribution.objects(**filters).first()

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

    @staticmethod
    def find_one(identifier: str):
        """
        Search a distribution by identifier in db
        """
        filters = dict(
            identifier=identifier
        )
        return Distribution.objects(**filters).first()
