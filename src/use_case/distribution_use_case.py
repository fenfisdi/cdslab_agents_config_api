from src.models.route_models.distribution import Distribution


class DistributionUseCase:

    @classmethod
    def validateDistribution(cls, distribution: Distribution):
        dist_type = distribution.dist_type.value
        if dist_type == "constant" or dist_type == "weights":
            distribution.dist_name = None
            distribution.filename = None
            distribution.kwargs = {}
        if dist_type == "empirical" or dist_type == "numpy":
            distribution.dist_name = None
            distribution.constant = None
