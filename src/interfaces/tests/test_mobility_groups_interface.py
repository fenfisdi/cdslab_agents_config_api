import uuid

from mongoengine import connect, disconnect
from unittest import TestCase

from src.models import MobilityGroup
from src.interfaces import MobilityGroupInterface


class MobilityGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="MobilityGroupInterfaceTestCase"
        )

        self.identifier = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.distribution_identifier = uuid.uuid1().hex
        self.name = "Mobility Group Unit Test"
        self.mobility_group = MobilityGroup(
            identifier=self.identifier,
            configuration=self.configuration_identifier,
            distribution=self.distribution_identifier,
            name=self.name
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        mobility_groups = \
            MobilityGroupInterface.find_all()

        self.assertIsNotNone(mobility_groups)

    def test_find_one(self):
        mobility_group = \
            MobilityGroupInterface.find_one(self.identifier)

        self.assertIsNotNone(mobility_group)

    def test_find_by_configuration(self):
        mobility_groups = \
            MobilityGroupInterface.find_by_configuration(
                self.configuration_identifier
            )

        self.assertIsNotNone(mobility_groups)
