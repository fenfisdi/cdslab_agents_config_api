import uuid

from mongoengine import connect, disconnect
from unittest import TestCase

from src.models import AgeGroup
from src.interfaces import AgeGroupInterface


class AgeGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="AgeGroupInterfaceTestCase"
        )

        self.identifier = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.name = "Age Group Unit Test"
        self.population_percentage = 23.5
        self.age_group = AgeGroup(
            identifier=self.identifier,
            configuration=self.configuration_identifier,
            name=self.name,
            population_percentage=self.population_percentage
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        age_groups = AgeGroupInterface.find_all()

        self.assertIsNotNone(age_groups)

    def test_find_one(self):
        age_group = AgeGroupInterface. \
            find_one(self.identifier)

        self.assertIsNotNone(age_group)
        self.assertEqual(
            age_group.identifier,
            self.identifier
        )

    def test_find_by_configuration(self):
        age_groups = AgeGroupInterface. \
            find_by_configuration(self.configuration_identifier)

        self.assertIsNotNone(age_groups)
