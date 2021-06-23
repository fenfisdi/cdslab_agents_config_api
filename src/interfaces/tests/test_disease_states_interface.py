from unittest import TestCase

from mongoengine import connect

from src.models.db.disease_states import DiseaseGroups


class DiseaseStatesTestCase(TestCase):
    def setUp(self) -> None:
        connect(
            "mongoenginetest",
            host="mongomock://localhost",
            alias="DiseaseStatesInterfaceTestCase"
        )
        
        self.disease_states = DiseaseGroups(
            name="Unit Test",
            can_get_infected=False,
            is_infected=False,
            can_spread=False,
            spread_radius=False,
            spread_probability=False
        ).save()
    
    def test_list_diseases_states(self):
        response = self.client.get(self.route)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
