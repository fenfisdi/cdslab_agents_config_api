from mongoengine import (
    DictField,
    EmbeddedDocument,
    EnumField,
    StringField,
    FloatField
)

from src.models.general import DistributionType


class Distribution(EmbeddedDocument):
    name = StringField()
    dist_type = EnumField(DistributionType, required=True)
    constant = FloatField()
    dist_name = StringField()
    filename = StringField()
    kwargs = DictField(null=True)
