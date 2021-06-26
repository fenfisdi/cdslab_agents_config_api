from datetime import datetime
from uuid import uuid1

from unittest import TestCase
from unittest.mock import patch, Mock

from mongoengine import connect, disconnect

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = "src.routes.susceptibility_groups"
    return ".".join([source, path])


class ListSusceptibilityGroupRouteTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="TestSusceptibilityGroupMongoDB"
        )
        from src.api import app
        self.client = TestClient(app)

        self.identifier = uuid1()
        self.conf_identifier = uuid1()
        self.distribution_identifier = uuid1()
        self.name = "Susceptibility Group Unit Test"
        self.distribution = dict(
            name="Distribution Test",
            distribution_type="constant",
            distribution_name="constant",
            distribution_filename="constant",
            distribution_extra_arguments=None
        )
        self.susceptibility_group = dict(
            identifier=self.identifier,
            distribution=self.distribution,
            name=self.name
        )
        self.route = f"/configuration/{self.conf_identifier}/" \
                     f"susceptibility_groups"

    def tearDown(self):
        disconnect()

    @patch(solve_path("SusceptibilityGroupInterface"))
    def test_find_susceptibility_groups_successful(
            self,
            susceptibility_groups_interface: Mock
    ):
        susceptibility_groups_interface.find_by_conf.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)

    @patch(solve_path("SusceptibilityGroupInterface"))
    def test_find_susceptibility_groups_fail(
            self,
            susceptibility_groups_interface: Mock
    ):
        susceptibility_groups_interface.find_by_conf.return_value = None

        response = self.client.get(self.route)

        self.assertIsNone(response)

    @patch(solve_path("ConfigurationInterface"))
    def test_create_susceptibility_group_success(
            self,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_name.return_value = Mock()

        response = self.client.post(
            url=self.route,
            json=self.new_configuration
        )

        self.assertIsNotNone(response)
