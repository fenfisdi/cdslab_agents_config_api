from src.models.db import Configuration, Population


class PopulationInterface:

    @staticmethod
    def find_one_by_conf(configuration: Configuration) -> Population:
        filters = dict(
            configuration=configuration,
        )
        return Population.objects(**filters).first()
