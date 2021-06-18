from uuid import UUID

from src.models.db import Configuration, User


class ConfigurationInterface:
    """
    Interface to consult configurations in DB
    """

    @staticmethod
    def find_all(user: User):
        """
        Find all configurations from a user.

        :param user: User authenticated
        """
        filters = dict(
            user=user,
            is_deleted=False,
        )
        return Configuration.objects(**filters).all()

    @staticmethod
    def find_by_identifier(identifier: UUID, user: User) -> Configuration:
        """
        Find configuration by identifier and user

        :param identifier: Identifier to search the configuration
        :param user: User authenticated.
        """
        filters = dict(
            identifier=identifier,
            user=user,
            is_deleted=False,
        )
        return Configuration.objects(**filters).first()

    @staticmethod
    def find_by_name(name: str, user: User) -> Configuration:
        """
        Find configuration by name, and user

        :param name: Name to search the configuration
        :param user: User authenticated
        """
        filters = dict(
            name=name,
            user=user,
            is_deleted=False,
        )
        return Configuration.objects(**filters).first()
