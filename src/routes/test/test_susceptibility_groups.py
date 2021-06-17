from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


route = "/susceptibility_groups"


def solve_path(path: str):
    source = "src.routes.susceptibility_groups"
    return ".".join([source, path])


class ListSusceptibilityGroupRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

    @patch(solve_path("SusceptibilityGroupInterface"))
    def test_find_all_successful(
            self,
            susceptibility_groups_interface: Mock
    ):
        susceptibility_groups_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("SusceptibilityGroupInterface"))
    def test_find_all_not_found(
            self,
            susceptibility_groups_interface: Mock
    ):
        susceptibility_groups_interface.find_all.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


