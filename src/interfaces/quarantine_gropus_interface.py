from src.models import QuarantineGroup


class QuarantineGroupInterface:
    """
    Interface to consult quarantine groups in db
    """

    @staticmethod
    def find_one(identifier: str):
        """
        Get a existing quarantine group in db

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return QuarantineGroup.objects(**filters).first()

    @staticmethod
    def find_all():
        """
        Get all existing quarantine groups in db
        """
        return QuarantineGroup.objects().all()

    @staticmethod
    def find_by_configuration(
            configuration_identifier: str
    ):
        """
        Get all existing quarantine groups by
        configuration in db
        """
        filters = dict(
            configuration=configuration_identifier
        )
        return QuarantineGroup.objects(**filters).all()
