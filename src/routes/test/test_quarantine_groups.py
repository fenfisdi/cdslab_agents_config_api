import uuid

from typing import List
from unittest import TestCase
from unittest.mock import patch, Mock
from mongoengine import connect, disconnect

from fastapi.testclient import TestClient

from src.models import QuarantineGroup

route = "/quarantine_groups"


def solve_path(path: str):
    source = "src.routes.quarantine_groups"
    return ".".join([source, path])


class ListQuarantineGroupRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.identifier_first = uuid.uuid1().hex
        self.identifier_second = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.name_first = "Quarantine Group Unit Test"
        self.name_second = "2Quarantine Group Unit Test"
        self.quarantine_group_first = QuarantineGroup(
            identifier=self.identifier_first,
            configuration=self.configuration_identifier,
            name=self.name_first
        )
        self.quarantine_group_second = QuarantineGroup(
            identifier=self.identifier_second,
            configuration=self.configuration_identifier,
            name=self.name_second
        )
        self.quarantine_groups_list = List
        self.quarantine_groups_list.append(self.age_group_first)
        self.quarantine_groups_list.append(self.age_group_second)

    def tearDown(self):
        disconnect()

    @patch(solve_path("QuarantineGroupInterface"))
    def test_find_all_successful(
            self,
            quarantine_group_interface: Mock
    ):
        quarantine_group_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("QuarantineGroupInterface"))
    def test_find_all_not_found(
            self,
            quarantine_group_interface: Mock
    ):
        quarantine_group_interface.find_all.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path("QuarantineGroupInterface"))
    def test_find_by_configuration_successful(
            self,
            quarantine_group_interface: Mock
    ):
        quarantine_group_interface. \
            find_by_configuration.return_value = Mock(
                to_mongo=Mock(return_value={})
            )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("QuarantineGroupInterface"))
    def test_find_by_configuration_not_found(
            self,
            quarantine_group_interface: Mock
    ):
        quarantine_group_interface. \
            find_by_configuration.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
