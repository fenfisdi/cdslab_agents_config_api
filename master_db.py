from os import environ
from uuid import uuid1

from mongoengine import connect

from src.models.db import RoleMachine
from src.models.db.master.distribution import MasterDistribution
from src.models.db.master.quarantine_restriction import QuarantineRestriction
from src.models.general import UserRole


def create_role_machines() -> None:
    try:
        # Create User default configuration
        RoleMachine(
            role=UserRole.USER,
            max_machine=5,
            default_memory=2046,
            default_cpu=2,
        ).save()
    except Exception as error:
        print(error)

    try:
        # Create Admin default configuration
        RoleMachine(
            role=UserRole.ADMIN,
            max_machine=10,
            default_memory=2046,
            default_cpu=2,
        ).save()
    except Exception as error:
        print(error)

    try:
        # Create Root default configuration
        RoleMachine(
            role=UserRole.ROOT,
            max_machine=10,
            default_memory=2046,
            default_cpu=2,
        ).save()
    except Exception as error:
        print(error)


if __name__ == "__main__":
    mongo_uri = environ.get("MONGO_URI")
    connect(host=mongo_uri)

    distributions = {
        "empirical": [
            {
                "parameter": "bandwidth",
                "type": "float",
                "values": None,
                "default_value": 1.0,
            },
            {
                "parameter": "algorithm",
                "type": None,
                "values": ["auto", "kd_tree", "ball_tree"],
                "default_value": "auto",
            },
            {
                "parameter": "kernel",
                "type": None,
                "values": [
                    "gaussian",
                    "tophat",
                    "epanechnikov",
                    "exponential",
                    "linear",
                    "cosine"
                ],
                "default_value": "gaussian",
            },
            {
                "parameter": "metric",
                "type": "str",
                "values": ["euclidean"],
                "default_value": "euclidean",
            },
            {
                "parameter": "atol",
                "type": "float",
                "values": None,
                "default_value": 0,
            },
            {
                "parameter": "rtol",
                "type": "float",
                "values": None,
                "default_value": 0,
            },
            {
                "parameter": "breadth_first",
                "type": "boolean",
                "values": ["True", "False"],
                "default_value": "True",
            },
            {
                "parameter": "leaf_size",
                "type": "int",
                "values": None,
                "default_value": 40,
            },
            {
                "parameter": "metric_params",
                "type": "dict",
                "values": None,
                "default_value": {},
            }
        ],
        "constant": [
            {
                "parameter": "type constant",
                "type": "int",
                "values": None,
                "default_value": 0,
            }
        ],
        "weights": [
            {
                "parameter": "bandwidth",
                "type": "float",
                "values": None,
                "default_value": 1.0,
            },
            {
                "parameter": "algorithm",
                "type": None,
                "values": ["auto", "kd_tree", "ball_tree"],
                "default_value": "auto",
            },
            {
                "parameter": "kernel",
                "type": None,
                "values": [
                    "gaussian",
                    "tophat",
                    "epanechnikov",
                    "exponential",
                    "linear",
                    "cosine"
                ],
                "default_value": "gaussian",
            },
            {
                "parameter": "metric",
                "type": "str",
                "values": ["euclidean"],
                "default_value": ["euclidean"],
            },
            {
                "parameter": "atol",
                "type": "float",
                "values": None,
                "default_value": 0,
            },
            {
                "parameter": "rtol",
                "type": "float",
                "values": None,
                "default_value": 0,
            },
            {
                "parameter": "breadth_first",
                "type": "boolean",
                "values": ["True", "False"],
                "default_value": "True",
            },
            {
                "parameter": "leaf_size",
                "type": "int",
                "values": None,
                "default_value": 40,
            }
        ],
        "numpy": [
            {
                "parameter": "normal",
                "type": "numpy",
                "values": [
                    {
                        "name": "loc",
                        "type": ["float", "List[float]"],
                    },
                    {
                        "name": "scale",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "lognormal",
                "type": "numpy",
                "values": [
                    {
                        "name": "mean",
                        "type": ["float", "List[float]"],
                    },
                    {
                        "name": "sigma",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "weibull",
                "type": "numpy",
                "values": [
                    {
                        "name": "a",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "gamma",
                "type": "numpy",
                "values": [
                    {
                        "name": "shape",
                        "type": ["float", "List[float]"],
                    },
                    {
                        "name": "scale",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "logistic",
                "type": "numpy",
                "values": [
                    {
                        "name": "loc",
                        "type": ["float", "List[float]"],
                    },
                    {
                        "name": "scale",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "poisson",
                "type": "numpy",
                "values": [
                    {
                        "name": "Iam",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "logseries",
                "type": "numpy",
                "values": [
                    {
                        "name": "P",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "geometric",
                "type": "numpy",
                "values": [
                    {
                        "name": "P",
                        "type": ["float", "List[float]"],
                    },
                ]
            },
            {
                "parameter": "hypergeometric",
                "type": "numpy",
                "values": [
                    {
                        "name": "ngoodint",
                        "type": ["int", "List[int]"],
                    },
                    {
                        "name": "nbad",
                        "type": ["int", "List[int]"],
                    },
                    {
                        "name": "nsample",
                        "type": ["int", "List[int]"],
                    },
                ]
            }
        ]
    }

    quarantine_restrictions = [
        {
            "name": "Cyclic quarantine restrictions",
            "type": "bool",
            "value": False
        },
        {
            "name": "Quarantine restrictions by tracing variables",
            "type": "bool",
            "value": False
        }
    ]

    for name, parameters in distributions.items():
        try:
            distribution = MasterDistribution(
                name=name,
                type=parameters
            ).save()

        except Exception as error:
            message = f"No fue posible insertar la distribución {name}, {error}"
            raise RuntimeError(message)

    for quarantine_restriction in quarantine_restrictions:
        try:
            QuarantineRestriction(
                identifier=uuid1(),
                name=quarantine_restriction["name"],
                type=quarantine_restriction["type"],
                value=quarantine_restriction["value"]
            ).save()
        except Exception as error:
            message = f"An error has been while insert {quarantine_restriction}"
            raise RuntimeError(message)

    create_role_machines()
