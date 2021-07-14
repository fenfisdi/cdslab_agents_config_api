import re
from typing import Optional

from fastapi import UploadFile

from src.models.db import Configuration, DiseaseGroup
from src.models.general import DistributionType, TypeFile
from src.services import FileAPI


class VerifyDistributionFile:
    EMPIRICAL_REGEX = r'^(\d+\n?)+$'
    WEIGHT_REGEX = r'^(\d+,\d+\n?)+$'

    @classmethod
    def handle(
        cls,
        file: UploadFile,
        distribution_type: DistributionType
    ) -> bool:
        regex_distributions = {
            DistributionType.EMPIRICAL: cls.EMPIRICAL_REGEX,
            DistributionType.WEIGHTS: cls.WEIGHT_REGEX,
        }
        regex = regex_distributions.get(distribution_type)
        text = file.file.read().decode('utf-8')
        if regex and not re.compile(regex).search(text):
            return False

        return True

    @classmethod
    def disease(
        cls,
        file: UploadFile,
        disease_state: DiseaseGroup
    ):
        disease_distribution = disease_state.distributions
        regex_distributions = {
            DistributionType.EMPIRICAL: cls.EMPIRICAL_REGEX,
            DistributionType.WEIGHTS: cls.WEIGHT_REGEX,
        }


class SaveDistributionFile:

    @classmethod
    def handle(
        cls,
        file: UploadFile,
        configuration: Configuration,
        name: str
    ) -> (Optional[dict], bool):
        header = 'application/octet-stream'

        text = file.file.read().decode('utf-8')
        file = [
            ('file', (f'{name}.csv', text, header))
        ]

        response, is_invalid = FileAPI.upload_file(
            configuration.identifier,
            file,
            file_type=TypeFile.UPLOADED
        )
        if is_invalid:
            return None, True

        return dict(id=response.get('data').get('uuid')), False
