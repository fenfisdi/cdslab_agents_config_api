from typing import Optional
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
    def find_one_by_id(identifier: UUID, user: User) -> Optional[Configuration]:
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
    def find_one_by_name(name: str, user: User) -> Optional[Configuration]:
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


class ConfigurationRootInterface:

    @classmethod
    def find_one_by_id(cls, identifier: UUID) -> Optional[Configuration]:
        filters = dict(
            identifier=identifier,
            is_deleted=False
        )
        return Configuration.objects(**filters).first()
