from mongoengine import (
    DictField,
    EmbeddedDocument,
    EnumField,
    StringField,
    UUIDField
)

from src.models.general import DistributionType


class Distribution(EmbeddedDocument):
    type = EnumField(DistributionType)
    numpy_type = StringField()
    file_id = UUIDField(binary=False, null=True, required=False)
    kwargs = DictField(null=True)
