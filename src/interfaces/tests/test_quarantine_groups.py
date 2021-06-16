import uuid

from mongoengine import connect, disconnect
from unittest import TestCase
ucm
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
        self.name = "Quarantine Group Unit Test"
        self.quarantine_group = QuarantineGroup(

        )
