from typing import Optional

from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.models.db.configuration import Configuration
from src.interfaces import ConfigurationInterface
from src.utils.messages import ConfigurationMessage
from src.utils.encoder import BsonObject
from src.utils.response import UJSONResponse


