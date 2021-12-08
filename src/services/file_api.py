from os import environ
from typing import Any, Tuple, Union
from uuid import UUID

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from .service import API, APIService
from ..models.general import TypeFile


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
            '/root/folder',
            json=body
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def upload_file(
        cls,
        simulation_uuid: UUID,
        files: Any = None,
        file_type: TypeFile = TypeFile.COMPUTED
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """

        :param simulation_uuid:
        :param files:
        :param file_type:
        """

        parameters = {
            'file_type': file_type.value,
        }
        response = cls.request.post(
            f'/root/simulation/{str(simulation_uuid)}/file',
            parameters=parameters,
            files=files
        )

        if not response.ok:
            return to_response(response), True
        return response.json(), False
