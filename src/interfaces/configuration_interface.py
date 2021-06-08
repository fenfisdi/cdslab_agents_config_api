from src.models.db.configuration import Configuration


class ConfigurationInterface:
    """
    Interface to consult configurations in DB
    """

    @staticmethod
    def find_all():
        """
        Get all configurations exists in db

        Return:
            Configurations object list
        """
        return Configuration.objects().objects().all()
