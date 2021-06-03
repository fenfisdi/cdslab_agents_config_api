from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import DistributionInterface
from src.models.db.Distribution import Distribution


class DistributionInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost', alias="DistributionInterfaceTestCase")

        self.distribution_not_found = "NotFound"
        self.distribution_name = "Constant"
        self.params_distribution = {"Parameter": "Type constant", "Type": "int", "Field": None}
        
        self.distribution = Distribution(
            name=self.distribution_name,
            type=[self.params_distribution]
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_parameters_successful(self):
        distribution = DistributionInterface.find_parameters(self.distribution_name)

        self.assertIsNotNone(distribution)
        self.assertDictEqual(distribution.type[0], self.params_distribution)

    def test_find_parameters_not_found(self):
        distribution = DistributionInterface.find_parameters(self.distribution_not_found)

        self.assertIsNone(distribution)
