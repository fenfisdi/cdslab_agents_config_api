class DiseaseStatesDistribution:
    
    disease_states_distribution = [
        "Daignosis",
        "Quarentine",
        "Hospitalization",
        "ICU"
    ]
    
    @classmethod
    def get_disease_states_distribution(cls):
        return disease_states_distribution
