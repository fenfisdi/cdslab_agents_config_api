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
        return Configuration.objects().all()

    @staticmethod
    def find_by_identifier(identifier: str):
        """
        Get a configuration by name

        Parameter:
            identifier (str): Identifier to search the configuration

        Return:
            A configuration object

        """
        filters = dict(
            identifier=identifier
        )
        return Configuration.objects(**filters).first()

    @staticmethod
    def find_by_name(name: str):
        """
        Get a configuration by name

        Parameter:
            name (str): Name to search the configuration

        Return:
            A configuration object

        """
        filters = dict(
            name=name
        )
        return Configuration.objects(**filters).first()
