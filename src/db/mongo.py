from os import environ

from mongoengine import connect

from src.utils.patterns import Singleton


class MongoEngine(metaclass=Singleton):
    def __init__(self):
        self.mongo_uri = "mongodb://cdsuser:cdspass@192.168.0.9:27017/cdslib_model?authSource=admin"  # environ.get("MONGO_URI")

    def get_connection(self):
        return connect(host=self.mongo_uri)
