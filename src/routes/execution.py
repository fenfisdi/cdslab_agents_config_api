from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import ConfigurationInterface, ConfigurationRootInterface
from src.models.general import ExecutionStatus
from src.use_case import (
    FindAgentInformation,
    FindMachineInformation,
    SecurityUseCase,
    SendAllInformation
)
from src.utils import ConfigurationMessage, DateTime, UJSONResponse
from src.utils.messages import ExecutionMessage

execution_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Execution"]
)


@execution_routes.post("/execute")
def execute_simulation(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    try:
        configuration_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not configuration_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        simulation_data = FindAgentInformation.handle(configuration_found)
        machine_data = FindMachineInformation.handle(user)

        is_invalid = SendAllInformation.handle(
            conf_uuid,
            user,
            simulation_data,
            machine_data
        )
        if is_invalid:
            return UJSONResponse(ExecutionMessage.invalid, HTTP_400_BAD_REQUEST)
        return UJSONResponse(ExecutionMessage.on_queue, HTTP_200_OK)

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@execution_routes.post("/finish")
def update_simulation_status(
    conf_uuid: UUID,
    status: ExecutionStatus = Query(...),
):
    try:
        configuration = ConfigurationRootInterface.find_one_by_id(conf_uuid)
        if not configuration:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        configuration.update(
            execution=dict(
                status=status,
                finish_date=DateTime.current_datetime(),
            )
        )

        return UJSONResponse(ConfigurationMessage.updated, HTTP_200_OK)

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
