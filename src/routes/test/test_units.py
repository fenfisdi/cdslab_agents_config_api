from unittest import TestCase

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = 'src.routes.units'
    return ".".join([source, path])


class GetUnitsRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = "/units/distance"
        self.route_units_time = "/units/time"

    def test_get_units_distance(self):
        response = self.client.get(self.route)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_get_units_time(self):
        response = self.client.get(self.route_units_time)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
