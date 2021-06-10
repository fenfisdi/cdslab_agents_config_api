from src.models.db.master.disease_states import MasterDiseaseStates


class DiseaseStatesInterface:
    """
    Interface to consult disease states in DB
    """
    @staticmethod
    def find_all():
        """
        Find all disease states

        Return:
            Disease States objects exist in bd as list
        """
        return MasterDiseaseStates.objects().all()
