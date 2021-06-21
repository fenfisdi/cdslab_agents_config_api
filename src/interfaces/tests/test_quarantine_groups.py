import uuid

from mongoengine import connect, disconnect
from unittest import TestCase
from src.models import QuarantineGroup
from src.interfaces import QuarantineGroupInterface


class QuarantineGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            'mongoenginetest',
            host='mongomock://localhost',
            alias="QuarantineGroupInterfaceTestCase"
        )
        self.identifier = uuid.uuid1().hex
        self.configuration_identifier = uuid.uuid1().hex
        self.name = "Quarantine Group Unit Test"
        self.quarantine_group = QuarantineGroup(
            identifier=self.identifier,
            configuration=self.configuration_identifier,
            name=self.name
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        quarantine_groups = \
            QuarantineGroupInterface.find_all()

        self.assertIsNotNone(quarantine_groups)

    def test_find_one(self):
        quarantine_groups = \
            QuarantineGroupInterface.find_by_identifier(self.identifier)

        self.assertIsNotNone(quarantine_groups)
        self.assertEqual(
            quarantine_groups.identifier,
            self.identifier
        )

    def test_find_by_configuration(self):
        age_groups = QuarantineGroupInterface. \
            find_by_configuration(self.configuration_identifier)

        self.assertIsNotNone(age_groups)
