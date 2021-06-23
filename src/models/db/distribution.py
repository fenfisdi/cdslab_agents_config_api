from mongoengine import DictField, EmbeddedDocument, EnumField, StringField

from src.models.general import DistributionType


class Distribution(EmbeddedDocument):
    name = StringField()
    distribution_type = EnumField(DistributionType, required=True)
    distribution_name = StringField()
    distribution_filename = StringField()
    distribution_extra_arguments = DictField(null=True)
