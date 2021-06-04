from typing import Optional, Union, List

from fastapi.responses import UJSONResponse as Response


class UJSONResponse(Response):
    '''
        Create the standard response for the endpoints 
    '''
    def __init__(
            self,
            message: str,
            status_code: int,
            data: Optional[Union[dict, List[dict]]] = None):
        '''
            Constructor of class
        Parameters:
            message (str): Response of process.
            status_code (int): HTTP code.
            data (dict, list): Data of process.
        '''
        response = dict(
            message=message,
            status_code=status_code,
            data=data,
        )
        super().__init__(response, status_code)