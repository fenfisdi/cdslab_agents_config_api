from mongoengine import (
    DictField,
    EmbeddedDocument,
    EnumField,
    UUIDField
)

from src.models.general import DistributionType


class Distribution(EmbeddedDocument):
    type = EnumField(DistributionType, required=True)
    file_id = UUIDField(binary=False, null=True, required=False)
    kwargs = DictField(null=True)
