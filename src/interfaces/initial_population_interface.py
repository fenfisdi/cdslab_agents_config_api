from src.models.db import(
    configuration,
    InitialPopulationSetup
)

class InitialPopulationInterface:
    """
    Interface to consult initial population setup in db
    """

    @staticmethod
    def find_by_configuration(config: configuration):
        """
        Find all existing initial population setup by configuration in db

        :param config: config information
        """
        filters=dict(
            configuration=config
        )
        return InitialPopulationSetup.objects(**filters).all()
