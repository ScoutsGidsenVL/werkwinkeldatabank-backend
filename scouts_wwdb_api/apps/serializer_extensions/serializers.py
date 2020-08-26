from rest_framework import serializers
from drf_yasg import openapi

# Overwrite DurationField to give it correct swagger configuration
class DurationField(serializers.DurationField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "format": "[DD] [HH:[MM:]]ss[.uuuuuu]",
        }
