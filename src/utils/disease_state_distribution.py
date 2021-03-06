class DiseaseStatesDistribution:
    
    disease_states_distribution = [
        "Diagnosis",
        "Quarantine",
        "Hospitalization",
        "ICU"
    ]
    
    @classmethod
    def get_disease_states_distribution(cls):
        return cls.disease_states_distribution
