from fastapi.testclient import TestClient
from unittest import TestCase


def solve_path(path: str):
    source = 'src.routes.disease_states'
    return ".".join([source, path])


class ListDiseaseStatesRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = "/diseaseStates"

    def test_list_disease_states_all(self):
        response = self.client.get(self.route)
        self.assertIsNotNone(response)
