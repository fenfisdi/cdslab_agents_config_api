from src.models import MobilityGroup


class MobilityGroupInterface:
    """
    Interface to consult mobility groups in db
    """

    @staticmethod
    def find_all():
        """
        Find all existing mobility groups in db
        """
        return MobilityGroup.objects().all()

    @staticmethod
    def find_one(identifier: str):
        """
        Find a existing mobility group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return MobilityGroup.objects(
            **filters
        ).first()

    @staticmethod
    def find_by_configuration(
            configuration_identifier: str
    ):
        filters = dict(
            configuration=configuration_identifier
        )
        return MobilityGroup.objects(
            **filters
        ).all()
