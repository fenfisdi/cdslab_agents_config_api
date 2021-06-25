import datetime

from uuid import uuid1

from unittest import TestCase
from unittest.mock import patch, Mock
from mongoengine import connect, disconnect
from fastapi.testclient import TestClient

from src.models.db import Configuration, User


def solve_path(path: str):
    source = "src.routes.age_groups"
    return ".".join([source, path])


class ListAgeGroupRouteTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="AgeGroupRotesTest"
        )

        from src.api import app
        self.client = TestClient(app)

        self.conf_identifier = uuid1()
        self.name_first = "Age Group Unit Test"
        self.name_second = "2Age Group Unit Test"
        self.population_percentage = 23.5
        self.route = f"/configuration/{self.conf_identifier}/age_groups"
        self.user = User(
            name="usert test",
            email="test@test.com"
        ).save().reload()
        self.configuration = Configuration(
            identifier=self.conf_identifier,
            name="string",
            population_number=0,
            interval_date={
                "start": datetime.datetime.now(),
                "end": datetime.datetime.now()
            },
            iteration_time_units="minutes",
            iteration_number=0,
            box_size={},
            distance_units="kilometers",
            user=self.user
        ).save().reload()

    def tearDown(self):
        disconnect()

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_successful(
            self,
            age_group_interface: Mock
    ):
        age_group_interface.find_by_configuration.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(
            self.route,
            headers={"token": "coneofsilence"}
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path("AgeGroupInterface"))
    def test_find_by_configuration_not_found(
            self,
            age_group_interface: Mock
    ):
        age_group_interface.find_by_configuration.return_value = None

        response = self.client.get(
            self.route,
            headers={"token": "coneofsilence"}
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path("AgeGroupInterface"))
    def test_create_age_group(self, age_group_interface: Mock):
        age_group_first = dict(
            name=self.name_first,
            population_percentage=self.population_percentage
        )
        age_group_second = dict(
            name=self.name_second,
            population_percentage=self.population_percentage
        )
        age_groups = list()
        age_groups.append(age_group_first)
        age_groups.append(age_group_second)

        response = self.client.post(
            self.route,
            age_groups,
            headers={"token": "coneofsilence"}
        )

        self.assertEqual(response.status_code, 201)
