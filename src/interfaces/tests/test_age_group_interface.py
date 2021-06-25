import datetime

from uuid import uuid1
from unittest import TestCase
from mongoengine import connect, disconnect

from src.models.db import AgeGroup, Configuration, User
from src.interfaces import AgeGroupInterface


class AgeGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
        )

        self.identifier = uuid1()
        self.configuration_identifier = uuid1()
        self.name = "Age Group Unit Test"
        self.population_percentage = 23.5
        self.user = User(
            name="usert test",
            email="test@test.com"
        ).save().reload()
        self.configuration = Configuration(
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
        self.age_group = AgeGroup(
            identifier=self.identifier,
            configuration=self.configuration,
            name=self.name,
            population_percentage=self.population_percentage
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one(self):
        age_group = AgeGroupInterface.find_one(
            self.identifier
        )

        self.assertIsNotNone(age_group)
        self.assertEqual(
            age_group.identifier,
            self.identifier
        )

    def test_find_by_configuration(self):
        age_groups = AgeGroupInterface.find_by_configuration(
            self.configuration_identifier
        )

        self.assertIsNotNone(age_groups)
