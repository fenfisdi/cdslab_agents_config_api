from os import environ
from typing import Tuple, Union
from uuid import UUID

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from .service import API, APIService


class FileAPI:
    api_url = environ.get('FILE_API')
    request = APIService(API(api_url))

    @classmethod
    def create_simulation_folder(
        cls,
        email: str,
        simulation_uuid: UUID,
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        body = {
            'email': email,
            'simulation_uuid': str(simulation_uuid),
        }
        response = cls.request.post(
            f'/root/folder',
            json=body
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False
