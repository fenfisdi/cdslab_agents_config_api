from uuid import UUID, uuid1

from fastapi import APIRouter, Depends, File, UploadFile
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import (
    ConfigurationInterface,
    DiseaseGroupInterface,
    NaturalHistoryInterface,
    VulnerabilityGroupInterface
)
from src.models.db import NaturalHistory
from src.models.general import DistributionType, NaturalDistributionType
from src.models.route_models import UpdateNaturalHistory
from src.use_case import (
    SaveDistributionFile,
    SaveNaturalHistoryDistributionFile,
    SaveNaturalHistoryTransitionFile,
    SecurityUseCase,
    VerifyDistributionFile,
    VerifyNaturalHistoryDistribution,
    VerifyNaturalHistoryTransition
)
from src.utils import BsonObject, UJSONResponse
from src.utils import NaturalHistoryMessage
from src.utils.messages import (
    ConfigurationMessage,
    DiseaseGroupMessage,
    DistributionMessage, VulnerabilityGroupMessage
)

natural_history_routes = APIRouter(
    prefix="/configuration/{conf_uuid}",
    tags=["Natural History"]
)


@natural_history_routes.put("/natural_history")
def update_natural_history(
    conf_uuid: UUID,
    natural_history: UpdateNaturalHistory,
    user = Depends(SecurityUseCase.validate)
):
    """
    Create or update natural history.

    \f
    :param conf_uuid: Configuration identifier.
    :param natural_history: Natural history to create in db.
    :param user: User authenticated.
    """
    try:
        config_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        vg_found = VulnerabilityGroupInterface.find_one_by_id(
            natural_history.vulnerability_group
        )
        if not vg_found:
            return UJSONResponse(
                VulnerabilityGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )
        dg_found = DiseaseGroupInterface.find_one(
            natural_history.disease_group
        )
        if not dg_found:
            return UJSONResponse(
                DiseaseGroupMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        nh_found = NaturalHistoryInterface.find_one(vg_found, dg_found)

        exclude_fields = {'vulnerability_group', 'disease_group'}
        if not nh_found:
            nh_found = NaturalHistory(
                **natural_history.dict(
                    exclude=exclude_fields
                ),
                configuration=config_found,
                vulnerability_group=vg_found,
                disease_group=dg_found,
                identifier=uuid1()
            )
            nh_found.save()

        else:
            nh_found.update(
                **natural_history.dict(
                    exclude=exclude_fields
                )
            )
            nh_found.distributions.update(
                natural_history.dict().get('distributions')
            )

        nh_found.reload()

        return UJSONResponse(
            NaturalHistoryMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(nh_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@natural_history_routes.get("/natural_history")
def list_natural_histories(
    conf_uuid: UUID,
    user = Depends(SecurityUseCase.validate)
):
    """
    Find all natural histories from configuration.

    \f
    :param conf_uuid: Configuration identifier.
    :param user: User authenticated.
    """

    config_found = ConfigurationInterface.find_one_by_id(
        conf_uuid,
        user
    )
    if not config_found:
        return UJSONResponse(
            ConfigurationMessage.not_found,
            HTTP_404_NOT_FOUND
        )

    natural_history_found = NaturalHistoryInterface.find_all_by_config(
        config_found
    )

    return UJSONResponse(
        NaturalHistoryMessage.found,
        HTTP_200_OK,
        BsonObject.dict(natural_history_found)
    )


@natural_history_routes.put("/natural_history/{uuid}/distribution/file")
def update_distribution_file(
    conf_uuid: UUID,
    uuid: UUID,
    distribution: NaturalDistributionType,
    file: UploadFile = File(...),
    user = Depends(SecurityUseCase.validate)
):
    try:
        config_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        nh_found = NaturalHistoryInterface.find_one_by_id(uuid, config_found)
        if not nh_found:
            return UJSONResponse(NaturalHistoryMessage.not_found, HTTP_200_OK)

        if not VerifyNaturalHistoryDistribution.handle(nh_found, distribution):
            return UJSONResponse(
                NaturalHistoryMessage.invalid_distribution,
                HTTP_400_BAD_REQUEST
            )

        distribution_found = nh_found.distributions.get(distribution.value)
        distribution_type = DistributionType[
            distribution_found.get("type", "").upper()
        ]

        if not VerifyDistributionFile.handle(file, distribution_type):
            return UJSONResponse(
                DistributionMessage.invalid,
                HTTP_400_BAD_REQUEST
            )

        data, is_invalid = SaveDistributionFile.handle(
            file,
            config_found,
            nh_found.id
        )
        if is_invalid:
            return UJSONResponse(
                DistributionMessage.can_not_save,
                HTTP_400_BAD_REQUEST
            )

        SaveNaturalHistoryDistributionFile.handle(
            nh_found,
            distribution,
            data.get("id")
        )

        return UJSONResponse(
            DistributionMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(nh_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)


@natural_history_routes.put("/natural_history/{uuid}/transition/file")
def update_transition_file(
    conf_uuid: UUID,
    uuid: UUID,
    state: str,
    file: UploadFile = File(...),
    user = Depends(SecurityUseCase.validate)
):
    try:
        config_found = ConfigurationInterface.find_one_by_id(
            conf_uuid,
            user
        )
        if not config_found:
            return UJSONResponse(
                ConfigurationMessage.not_found,
                HTTP_404_NOT_FOUND
            )

        nh_found = NaturalHistoryInterface.find_one_by_id(uuid, config_found)
        if not nh_found:
            return UJSONResponse(NaturalHistoryMessage.not_found, HTTP_200_OK)

        if not VerifyNaturalHistoryTransition.handle(nh_found, state):
            return UJSONResponse(
                NaturalHistoryMessage.invalid_transition,
                HTTP_400_BAD_REQUEST
            )
        distribution_found = nh_found.transitions.get(state)
        distribution_type = DistributionType[
            distribution_found.get("distribution", {}).get("type", "").upper()
        ]

        if not VerifyDistributionFile.handle(file, distribution_type):
            return UJSONResponse(
                DistributionMessage.invalid,
                HTTP_400_BAD_REQUEST
            )

        data, is_invalid = SaveDistributionFile.handle(
            file,
            config_found,
            f"{nh_found.id}"
        )
        if is_invalid:
            return UJSONResponse(
                DistributionMessage.can_not_save,
                HTTP_400_BAD_REQUEST
            )

        SaveNaturalHistoryTransitionFile.handle(
            nh_found,
            state,
            data.get("id")
        )

        return UJSONResponse(
            DistributionMessage.updated,
            HTTP_200_OK,
            BsonObject.dict(nh_found)
        )

    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
