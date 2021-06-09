import uuid

from mongoengine import connect, disconnect
from unittest import TestCase

from src.models import Configuration
from src.interfaces import ConfigurationInterface


class ConfigurationInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            'mongoenginetest',
            host='mongomock://localhost',
            alias="ConfigurationInterfaceTestCase"
        )

        self.identifier = uuid.uuid1().hex
        self.name = "Configuration Unit Test"
        self.configuration = Configuration(
            identifer=self.identifier,
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

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        configurations = ConfigurationInterface.find_all()

        self.assertIsNotNone(configurations)

    def test_find_by_identifier(self):
        configuration = ConfigurationInterface.find_by_identifier(self.identifier)

        self.assertIsNotNone(configuration)
        self.assertEqual(configuration.identifer, self.identifier)

    def test_find_by_name(self):
        configuration = ConfigurationInterface.find_by_name(self.name)

        self.assertIsNotNone(configuration)
        self.assertEqual(configuration.name, self.name)
