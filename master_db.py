from os import environ
from mongoengine import connect

from src.models.db.Distribution import Distribution

if __name__ == "__main__":

    mongo_uri = environ.get('MONGO_URI')
    connect(host=mongo_uri)

    distributions =["Constant", "Empirical", "Weigths", "Numpy"]
    parameters = { 
                "Empirical": [{"Parameter": "bandwidth", "Type": "float", "Field": [1.0]},
                          {"Parameter": "algorithm", "Type": None, "Field": ["auto", "kd_tree", "ball_tree"]},
                          {"Parameter": "kernel", "Type": None, "Field": ["gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"]},
                          {"Parameter": "metric", "Type": "str", "Field": ["euclidean"]},
                          {"Parameter": "atol", "Type": "float", "Field": [0]},
                          {"Parameter": "rtol", "Type": "float", "Field": [0]},
                          {"Parameter": "breadth_first", "Type": "boolean", "Field": ["True", "False"]},
                          {"Parameter": "leaf_size", "Type": "int", "Field": [40]},
                          {"Parameter": "metric_params", "Type": "dict", "Field": [None]} ],
                "Constant": [{"Parameter": "Type constant", "Type": "int", "Field": [None]}],
                "Weigths": [{"Parameter": "bandwidth", "Type": "float", "Field": [1.0]},
                          {"Parameter": "algorithm", "Type": None, "Field": ["auto", "kd_tree", "ball_tree"]},
                          {"Parameter": "kernel", "Type": None, "Field": ["gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"]},
                          {"Parameter": "metric", "Type": "str", "Field": ["euclidean"]},
                          {"Parameter": "atol", "Type": "float", "Field": [0]},
                          {"Parameter": "rtol", "Type": "float", "Field": [0]},
                          {"Parameter": "breadth_first", "Type": "boolean", "Field": ["True", "False"]},
                          {"Parameter": "leaf_size", "Type": "int", "Field": [40]}],
                "Numpy": [{"Parameter": "normal", "Type": "numpy", "Field": {
                                        "name": "loc", "type":["float", "List[float]"], 
                                        "name": "scale", "type":["float", "List[float]"]}},
                          {"Parameter": "lognormal", "Type": "numpy", "Field": {
                                        "name": "mean", "type":["float", "List[float]"],
                                        "name": "sigma", "type":["float", "List[float]"],}},
                          {"Parameter": "weibull", "Type": "numpy", "Field": {
                                        "name": "a", "type":["float", "List[float]"]}},
                          {"Parameter": "gamma", "Type": "numpy", "Field": {
                                        "name": "shape", "type":["float", "List[float]"],
                                        "name": "scale", "type":["float", "List[float]"]}},
                          {"Parameter": "logistic", "Type": "numpy", "Field": {
                                        "name": "loc", "type":["float", "List[float]"], 
                                        "name": "scale", "type":["float", "List[float]"]}},
                          {"Parameter": "poisson", "Type": "numpy", "Field": {
                                        "name": "Iam", "type":["float", "List[float]"]}},
                          {"Parameter": "logseries", "Type": "numpy", "Field": {
                                        "name": "P", "type":["float", "List[float]"]}},
                          {"Parameter": "geometric", "Type": "numpy", "Field": {
                                        "name": "P", "type":["float", "List[float]"]}},
                          {"Parameter": "hypergeometric", "Type": "numpy", "Field": {
                                        "name": "ngoodint", "type":["int", "List[int]"],
                                        "name": "nbad", "type":["int", "List[int]"],
                                        "name": "nsample", "type":["int", "List[int]"]}}]  
                }

    for name in distributions:
        try:
            distribution = Distribution()
            distribution.name = name
            distribution.type = parameters[name]

            distribution.save()

            print(f"{name} insertada correctamente")
        except Exception as error:
            print(f"No fue posible insertar {name}")
            print(error)