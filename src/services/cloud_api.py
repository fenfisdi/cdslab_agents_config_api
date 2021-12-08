from os import environ
from typing import Tuple, Union

from src.utils.response import UJSONResponse, to_response
from .service import API, APIService


class CloudAPI:
    api_url = environ.get('CLOUD_API')
    request = APIService(API(api_url))

    @classmethod
    def execute_simulation(
        cls,
        data: dict,
        token: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = cls.request.post(
            '/root/simulation/execute',
            headers=headers,
            json=data
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False
