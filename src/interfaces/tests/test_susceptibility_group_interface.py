from datetime import datetime
from uuid import uuid1
from unittest import TestCase

from mongoengine import connect, disconnect

from src.models.db import (
    SusceptibilityGroup,
    Configuration,
    User,
    Distribution
)
from src.interfaces import SusceptibilityGroupInterface


class SusceptibilityGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
        )

        self.identifier = uuid1()
        self.conf_identifier = uuid1()
        self.distribution_identifier = uuid1()
        self.name = "Susceptibility Group Unit Test"
        self.distribution = Distribution(
            name="Distribution Test",
            distribution_type="constant",
            distribution_name = "constant",
            distribution_filename = "constant",
            distribution_extra_arguments=None
        )
        self.user = User(
            name="usert test",
            email="test@test.com"
        ).save().reload()
        self.configuration = Configuration(
            identifier=self.conf_identifier,
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
        self.susceptibility_group = SusceptibilityGroup(
            identifier=self.identifier,
            configuration=self.configuration,
            distribution=self.distribution,
            name=self.name
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one(self):
        age_group = SusceptibilityGroupInterface.find_one(
            self.identifier
        )

        self.assertIsNotNone(age_group)
        self.assertEqual(
            age_group.identifier,
            self.identifier
        )

    def test_find_by_configuration(self):
        age_groups = SusceptibilityGroupInterface.find_by_conf(
            self.configuration
        )

        self.assertIsNotNone(age_groups)
