from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = 'src.routes.distributions'
    return ".".join([source, path])


class GetDistributionsTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.distribution = "Constant"
        self.distribution_not_found = "not_found"
        self.route_distributions = "/distributions"
        self.route_distributions_params = f"/distributions/parameters/{self.distribution}"
        self.route_distributions_params_not_found = f"/distributions/parameters/{self.distribution_not_found}"

    @patch(solve_path('DistributionInterface'))
    def test_list_distributions(self, distribution_interface: Mock):
        distribution_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route_distributions)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('DistributionInterface'))
    def test_parameters_successful(self, distribution_interface: Mock):
        distribution_interface.find_parameters.return_value = Mock(
            to_mongo=Mock(return_value={})
            )

        response = self.client.get(self.route_distributions_params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('DistributionInterface'))
    def test_parameters_not_found(self, distribution_interface: Mock):
        distribution_interface.find_parameters.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route_distributions_params_not_found)

        self.assertIsNotNone(response)
