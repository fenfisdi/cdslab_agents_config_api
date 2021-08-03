import uuid
from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import SusceptibilityGroupInterface
from src.models import SusceptibilityGroup


class SusceptibilityGroupInterfaceTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="SusceptibilityGroupInterfaceTestCase"
        )

        self.identifier = uuid.uuid1()
        self.configuration_identifier = uuid.uuid1()
        self.distribution_identifier = uuid.uuid1()
        self.name = "Susceptibility Group Unit Test"
        self.susceptibility_group = SusceptibilityGroup(
            identifier=self.identifier,
            configuration=self.configuration_identifier,
            distribution=self.distribution_identifier,
            name=self.name
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_all(self):
        susceptibility_groups = SusceptibilityGroupInterface.find_all()

        self.assertIsNotNone(susceptibility_groups)

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
        age_groups = SusceptibilityGroupInterface.find_all_by_conf(
            self.configuration_identifier
        )

        self.assertIsNotNone(age_groups)
