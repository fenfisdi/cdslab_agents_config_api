import uuid

from typing import List
from unittest import TestCase
from unittest.mock import patch, Mock
from mongoengine import connect, disconnect

from fastapi.testclient import TestClient

from src.models import AgeGroup

route = "/age_groups"


def solve_path(path: str):
    source = "src.routes.age_groups"
    return ".".join([source, path])


class ListAgeGroupRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.identifier_first = uuid.uuid1().hex
        self.identifier_second = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.name_first = "Age Group Unit Test"
        self.name_second = "2Age Group Unit Test"
        self.population_percentage = 23.5
        self.age_group_first = AgeGroup(
            identifier=self.identifier_first,
            configuration=self.configuration_identifier,
            name=self.name_first,
            population_percentage=self.population_percentage
        )
        self.age_group_second = AgeGroup(
            identifier=self.identifier_second,
            configuration=self.configuration_identifier,
            name=self.name_second,
            population_percentage=self.population_percentage
        )
        self.age_groups_list = List
        self.age_groups_list.append(self.age_group_first)
        self.age_groups_list.append(self.age_group_second)

    def tearDown(self):
        disconnect()

    @patch(solve_path("AgeGroupInterface"))
    def test_find_all_successful(
            self,
            age_group_interface: Mock
    ):
        age_group_interface.find_all.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_all_not_found(
            self,
            age_group_interface: Mock
    ):
        age_group_interface.find_all.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_successful(
            self,
            age_group_interface: Mock
    ):
        age_group_interface. \
            find_by_configuration.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_not_found(
            self,
            age_group_interface: Mock
    ):
        age_group_interface. \
            find_by_configuration.return_value = None

        response = self.client.get(route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
