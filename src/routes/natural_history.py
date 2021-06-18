from fastapi import APIRouter
from starlette.status import HTTP_200_OK, \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.utils import BsonObject, UJSONResponse

natural_history_routes = APIRouter(tags=["NatualHistory"])

@natural_history_routes.post("/natualHistory")
def save():
    pass