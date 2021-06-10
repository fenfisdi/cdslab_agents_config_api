from os import environ
from mongoengine import connect
from uuid import uuid1

from src.models.db.master.distribution import MasterDistribution
from src.models.db.master.disease_states import MasterDiseaseStates

if __name__ == "__main__":

    mongo_uri = environ.get("MONGO_URI")
    connect(host=mongo_uri)

    disease_status = [
        "diagnosis",
        "quarantine_postdiagnosis",
        "hospitalization_prob",
        "ICU_prob"
    ]

    type_float_list = [
        "float",
        "List[float]"
    ]

    type_int_list = [
        "int",
        "List[int]"
    ]

    numpy_normal_field_loc = {
        "name": "loc",
        "type": type_float_list
    }
    numpy_normal_field_scale = {
        "name": "scale",
        "type": type_float_list
    }

    numpy_log_normal_field_mean = {
        "name": "mean",
        "type": type_float_list
    }

    numpy_log_normal_field_sigma = {
        "name": "sigma",
        "type": type_float_list
    }

    numpy_gamma_field_shape = {
        "name": "shape",
        "type": type_float_list
    }

    numpy_gamma_field_scale = {
        "name": "scale",
        "type": type_float_list
    }

    numpy_logistic_field_loc = {
        "name": "loc",
        "type": type_float_list
    }

    numpy_logistic_field_scale = {
        "name": "scale",
        "type": type_float_list
    }

    numpy_hyper_geometric_field_n_good_int = {
        "name": "ngoodint",
        "type": type_float_list
    }

    numpy_hyper_geometric_field_n_bad = {
        "name": "nbad",
        "type": type_int_list
    }

    numpy_hyper_geometric_field_n_sample = {
        "name": "nsample",
        "type": type_int_list
    }

    distributions = {
        "Empirical": [
            {
                "Parameter": "bandwidth",
                "Type": "float",
                "Field": [1.0]},
            {
                "Parameter": "algorithm",
                "Type": None,
                "Field": [
                    "auto",
                    "kd_tree",
                    "ball_tree"
                ]
            },
            {
                "Parameter": "kernel",
                "Type": None,
                "Field": [
                    "gaussian",
                    "tophat",
                    "epanechnikov",
                    "exponential",
                    "linear",
                    "cosine"
                ]
            },
            {
                "Parameter": "metric",
                "Type": "str",
                "Field": ["euclidean"]
            },
            {
                "Parameter": "atol",
                "Type": "float",
                "Field": [0]
            },
            {
                "Parameter": "rtol",
                "Type": "float",
                "Field": [0]
            },
            {
                "Parameter": "breadth_first",
                "Type": "boolean",
                "Field": ["True", "False"]
            },
            {
                "Parameter": "leaf_size",
                "Type": "int",
                "Field": [40]
            },
            {
                "Parameter": "metric_params",
                "Type": "dict",
                "Field": [None]
            }
        ],
        "Constant": [
            {
                "Parameter": "Type constant",
                "Type": "int",
                "Field": [None]
            }
        ],
        "Weigths": [
            {
                "Parameter": "bandwidth",
                "Type": "float",
                "Field": [1.0]
            },
            {
                "Parameter": "algorithm",
                "Type": None,
                "Field": [
                    "auto",
                    "kd_tree",
                    "ball_tree"
                ]
            },
            {
                "Parameter": "kernel",
                "Type": None,
                "Field": [
                    "gaussian",
                    "tophat",
                    "epanechnikov",
                    "exponential",
                    "linear",
                    "cosine"
                ]
            },
            {
                "Parameter": "metric",
                "Type": "str",
                "Field": ["euclidean"]
            },
            {
                "Parameter": "atol",
                "Type": "float",
                "Field": [0]
            },
            {
                "Parameter": "rtol",
                "Type": "float",
                "Field": [0]
            },
            {
                "Parameter": "breadth_first",
                "Type": "boolean",
                "Field": ["True", "False"]
            },
            {
                "Parameter": "leaf_size",
                "Type": "int",
                "Field": [40]
            }
        ],
        "Numpy": [
            {
                "Parameter": "normal",
                "Type": "numpy",
                "Field": {
                    numpy_normal_field_loc,
                    numpy_normal_field_scale
                }
            },
            {
                "Parameter": "lognormal",
                "Type": "numpy",
                "Field": {
                    numpy_log_normal_field_mean,
                    numpy_log_normal_field_sigma
                }
            },
            {
                "Parameter": "weibull",
                "Type": "numpy",
                "Field": {
                    "name": "a",
                    "type": type_float_list
                }
            },
            {
                "Parameter": "gamma",
                "Type": "numpy",
                "Field": {
                    numpy_gamma_field_shape,
                    numpy_gamma_field_scale
                }
            },
            {
                "Parameter": "logistic",
                "Type": "numpy",
                "Field": {
                    numpy_logistic_field_loc,
                    numpy_logistic_field_scale
                }
            },
            {
                "Parameter": "poisson",
                "Type": "numpy",
                "Field": {
                    "name": "Iam",
                    "type": type_float_list
                }
            },
            {
                "Parameter": "logseries",
                "Type": "numpy",
                "Field": {
                    "name": "P",
                    "type": type_float_list
                }
            },
            {
                "Parameter": "geometric",
                "Type": "numpy",
                "Field": {
                    "name": "P",
                    "type": type_float_list
                }
            },
            {
                "Parameter": "hypergeometric",
                "Type": "numpy",
                "Field": {
                    numpy_hyper_geometric_field_n_good_int,
                    numpy_hyper_geometric_field_n_bad,
                    numpy_hyper_geometric_field_n_sample
                }
            }
        ]
    }

    for name, parameters in distributions.items():
        try:
            distribution = MasterDistribution(
                name=name,
                type=parameters).save()

        except Exception as error:
            raise Exception(f"An error has been occurred while MasterDistribution saved")

    for name in disease_status:
        try:
            MasterDiseaseStates(
                identifer=uuid1().hex,
                name=name
            ).save()

        except Exception as error:
            raise Exception(f"An error has been occurred while MasterDiseaseStates saved")
