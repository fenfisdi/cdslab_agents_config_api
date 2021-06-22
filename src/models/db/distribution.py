from mongoengine import DictField, EmbeddedDocument, StringField


class Distribution(EmbeddedDocument):
    name = StringField(required=True)
    distribution_type = StringField(required=True)
    distribution_name = StringField()
    distribution_filename = StringField()
    distribution_extra_arguments = DictField(null=True)
