from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = "src.routes.configuration"
    return ".".join([source, path])


class CreateConfigurationRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = "/configuration"
        self.name = "Configuration Unit Test"

        self.new_configuration = dict(
            name=self.name,
            population_number=80,
            interval_date=dict(
                start="2021-06-08T22:01:43.000444",
                end="2021-06-09T09:00:43.000444"
            ),
            iteration_time_units="min",
            iteration_number=20,
            box_size=dict(
                horizontal=50,
                vertical=99
            ),
            distance_units="ft",
            is_delete=False
        )

    @patch(solve_path("ConfigurationInterface"))
    def test_create_configuration_successful(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_name.return_value = None

        response = self.client.post(
            url=self.url,
            json=self.new_configuration
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

    @patch(solve_path("ConfigurationInterface"))
    def test_create_configuration_exist(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_name.return_value = Mock()

        response = self.client.post(
            url=self.url,
            json=self.new_configuration
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class UpdateConfigurationRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = "/configuration"

        self.update_configuration = dict(
            name="Other name"
        )

    @patch(solve_path("ConfigurationInterface"))
    def test_update_configuration_successful(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_identifier.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.put(
            self.route,
            json=self.update_configuration
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("ConfigurationInterface"))
    def test_update_configuration_not_found(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_identifier.return_value = None

        response = self.client.put(
            self.route,
            json=self.update_configuration
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


class FindConfigurationRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = "/configuration"

    @patch(solve_path("ConfigurationInterface"))
    def test_find_all_successful(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("ConfigurationInterface"))
    def test_find_all_not_found(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_all.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
