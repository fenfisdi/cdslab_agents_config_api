from uuid import uuid1

from typing import List
from unittest import TestCase
from unittest.mock import patch, Mock
from mongoengine import connect, disconnect

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = "src.routes.mobility_groups"
    return ".".join([source, path])


class ListMobilityGroupRoteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.conf_identifier = uuid1()
        self.route = f"/configuration/{self.conf_identifier}/mobility_groups"

    def tearDown(self):
        disconnect()

    @patch(solve_path("MobilityGroupInterface"))
    @patch(solve_path("ConfigurationInterface"))
    def test_list_mobility_groups_successful(
            self,
            mobility_group_interface: Mock,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_identifier.return_value = Mock(
            to_mongo=Mock(return_value={})
        )
        mobility_group_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("MobilityGroupInterface"))
    @patch(solve_path("ConfigurationInterface"))
    def test_list_mobility_groups_fail(
            self,
            mobility_group_interface: Mock,
            configuration_interface: Mock
    ):
        configuration_interface.find_by_identifier.return_value = None
        mobility_group_interface.find_all.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
