from datetime import datetime
from uuid import uuid1

from mongoengine import connect, disconnect
from unittest.mock import patch, Mock
from unittest import TestCase

from src.models.db import MobilityGroup, Configuration, User
from src.interfaces import MobilityGroupInterface


class MobilityGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
        )

        self.identifier = uuid1()
        self.conf_identifier = uuid1()
        self.user = User(
            name="usert test",
            email="test@test.com"
        ).save().reload()
        self.configuration = Configuration(
            identifier=self.conf_identifier,
            name="Conf test",
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
        ).save().reload()
        self.distribution = dict(
            name="Distribution Test",
            distribution_type="constant",
            distribution_name="Distribution name test",
            distribution_filename="Distribution filename test",
            distribution_extra_arguments=dict()
        )
        self.mobility_group = MobilityGroup(
            identifier=self.identifier,
            configuration=self.configuration,
            distribution=self.distribution,
            name="Mobility Group Unit Test"
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_all_successful(self):
        mobility_groups = MobilityGroupInterface.find_all.return_value = Mock()

        self.assertIsNotNone(mobility_groups)

    def test_find_all_fail(self):
        mobility_groups = MobilityGroupInterface.find_all.return_value = None

        self.assertIsNone(mobility_groups)

    def test_find_one_successful(self):
        mobility_group = MobilityGroupInterface.find_one.return_value = Mock()

        self.assertIsNotNone(mobility_group)

    def test_find_one_fail(self):
        mobility_group = MobilityGroupInterface.find_one.return_value = None

        self.assertIsNone(mobility_group)

    def test_find_by_configuration_successful(self):
        mobility_groups = \
            MobilityGroupInterface.find_by_configuration.return_value = Mock()

        self.assertIsNotNone(mobility_groups)

    def test_find_by_configuration_fail(self):
        mobility_groups = \
            MobilityGroupInterface.find_by_configuration.return_value = None

        self.assertIsNone(mobility_groups)
