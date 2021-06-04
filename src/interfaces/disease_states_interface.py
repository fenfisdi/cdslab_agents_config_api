from src.models.db.master.disease_states import MasterDiseaseStates

class DiseaseStatesInterface:
    '''
        Interface to consult disease states in DB
    '''
    @staticmethod
    def fin_all():
        """
        Find all disease states
        """
        return MasterDiseaseStates.objects().all()