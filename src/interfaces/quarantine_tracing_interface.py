from uuid import UUID

from src.models import (
    Configuration,
    QuarantineTracing
)


class QuarantineTracingInterface:
    """
    Interface to consult QuarantineTracing in db
    """

    @staticmethod
    def find_by_identifier(identifier: UUID):
        """
        Find a quarantine tracing by identifier

        :param identifier: Identifier to search
        """
        filters = dict(
            identifier=identifier
        )
        return QuarantineTracing.objects(**filters).first()

    @staticmethod
    def find_by_conf(conf: Configuration):
        """
        Find all quarantine tracing by configuration

        :param conf: Configuration to search
        """
        filters = dict(
            configuration=conf
        )
        return QuarantineTracing.objects(**filters).all()
