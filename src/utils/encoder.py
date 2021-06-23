from datetime import datetime
from json import JSONEncoder
from typing import Union

from bson import DBRef, ObjectId
from mongoengine import Document, QuerySet
from ujson import loads


class BsonEncoder(JSONEncoder):
    """
    Class that allows conversion to JSON
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, DBRef):
            return str(o.id)
        return JSONEncoder.default(self, o)


class BsonObject:
    """
        Transform a mongodb document into a dictionary
    """

    @classmethod
    def dict(
        cls, 
        document: Union[Document, Document],
        get_type = False
    ):
        """
        Creates a python dictionary based in a mongodb document
        
        :param document: Mongodb document to transform
        :param get_type: Handler the filter keys
        """
        if isinstance(document, QuerySet):
            document = [value.to_mongo() for value in document]
            raw = BsonEncoder().encode(document)
        else:
            raw = BsonEncoder().encode(document.to_mongo())
        document_dict = loads(raw)

        if isinstance(document_dict, dict):
            return cls.__filter_keys(document_dict, get_type)
        if isinstance(document_dict, list):
            return [cls.__filter_keys(document, get_type) for document in document_dict]
        raise TypeError('Invalid Type')

    @classmethod
    def __filter_keys(cls, data: dict, get_type: bool) -> dict:
        """
        Remove sensitive data from the dictionary
        
        :param data: Dictionary with data to filter
        """
        invalid_keys = {
            "_id", "_cls", "inserted_at", "updated_at", "is_deleted"
        }

        invalid_keys.remove("_cls") if get_type \
            else invalid_keys

        for k in data.copy().keys():
            if k in invalid_keys:
                del data[k]
        return data