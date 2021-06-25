from datetime import datetime

from uuid import uuid1

from mongoengine import connect, disconnect
from unittest import TestCase

from src.models.db import Configuration, User
from src.interfaces import ConfigurationInterface


class ConfigurationInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost"
        )

        self.identifier = uuid1()
        self.name = "Configuration Unit Test"
        self.user = User(
            name="usert test",
            email="test@test.com"
        ).save().reload()
        self.configuration = Configuration(
            identifier=self.identifier,
            name=self.name,
            population_number=80,
            interval_date=dict(
                start=datetime.now(),
                end=datetime.now()
            ),
            iteration_time_units="minutes",
            iteration_number=20,
            box_size=dict(
                horizontal=50,
                vertical=99
            ),
            distance_units="kilometers",
            is_deleted=False,
            user=self.user
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_by_identifier(self):
        configuration = ConfigurationInterface.find_by_identifier(
            self.identifier,
            self.user
        )

        self.assertIsNotNone(configuration)
        self.assertEqual(
            configuration.identifier,
            self.identifier
        )

    def test_find_by_name(self):
        configuration = ConfigurationInterface.find_by_name(
            self.name,
            self.user
        )

        self.assertIsNotNone(configuration)
        self.assertEqual(
            configuration.name,
            self.name
        )
