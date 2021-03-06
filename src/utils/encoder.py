from datetime import datetime
from json import JSONEncoder
from typing import List, Optional, Union

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
        document: Union[List[Document], Document]
    ) -> Optional[Union[List[dict], dict]]:
        """
        Creates a python dictionary based in a mongodb document
        
        :param document: Mongodb document to transform
        """
        if not document:
            return None
        if isinstance(document, QuerySet) or isinstance(document, list):
            if not document:
                return None
            document = [value.to_mongo() for value in document]
            raw = BsonEncoder().encode(document)
        else:
            raw = BsonEncoder().encode(document.to_mongo())
        document_dict = loads(raw)

        if isinstance(document_dict, dict):
            return cls.__filter_keys(document_dict)
        if isinstance(document_dict, list):
            return [cls.__filter_keys(document) for document in document_dict]
        raise TypeError('Invalid Type')

    @classmethod
    def __filter_keys(cls, data: dict) -> dict:
        """
        Remove sensitive data from the dictionary
        
        :param data: Dictionary with data to filter
        """
        invalid_keys = {
            "_id", "_cls", "inserted_at", "updated_at", "is_deleted"
        }

        for k in data.copy().keys():
            if k in invalid_keys:
                del data[k]
        return data
