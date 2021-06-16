from src.models.db.configuration import Configuration


class ConfigurationInterface:
    """
    Interface to consult configurations in DB
    """

    @staticmethod
    def find_all():
        """
        Get all existing configurations in db
        """
        return Configuration.objects().all()

    @staticmethod
    def find_by_identifier(identifier: str):
        """
        Get a configuration by identifier

        :param identifier: Identifier to search the configuration
        """
        filters = dict(
            identifier=identifier
        )
        return Configuration.objects(**filters).first()

    @staticmethod
    def find_by_name(name: str):
        """
        Get a configuration by name

        :param name: Name to search the configuration
        """
        filters = dict(
            name=name
        )
        return Configuration.objects(**filters).first()
