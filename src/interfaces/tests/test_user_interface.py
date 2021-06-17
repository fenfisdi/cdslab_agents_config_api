from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import UserInterface
from src.models.db import User


class UserInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.user = User(
            name="test user",
            email="test@test.com"
        )
        self.user.save()

    def tearDown(self):
        disconnect()

    def test_user_found(self):
        result = UserInterface.find_one('test@test.com')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, User)

    def test_user_not_found(self):
        result = UserInterface.find_one('any@email.com')

        self.assertIsNone(result)
