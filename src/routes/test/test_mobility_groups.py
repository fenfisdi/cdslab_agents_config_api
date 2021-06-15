import uuid

from typing import List
from unittest import TestCase
from unittest.mock import patch, Mock
from mongoengine import connect, disconnect

from fastapi.testclient import TestClient

from src.models import MobilityGroup


route = "/mobility_groups"


def solve_path(path: str):
    source = "src.routes.mobility_groups"
    return ".".join([source, path])


class ListMobilityGroupRoteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.identifier = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.distribution_identifier = uuid.uuid1().hex

    @patch(solve_path("AgeGroupInterface"))
    def test_find_all_successful(
            self,
            mobility_group_interface: Mock
    ):
        mobility_group_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_all_not_found(
            self,
            mobility_group_interface: Mock
    ):
        mobility_group_interface.find_all.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_successful(
            self,
            mobility_group_interface: Mock
    ):
        mobility_group_interface. \
            find_by_configuration.return_value = Mock(
                to_mongo=Mock(return_value={})
            )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_not_found(
            self,
            mobility_group_interface: Mock
    ):
        mobility_group_interface. \
            find_by_configuration.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
