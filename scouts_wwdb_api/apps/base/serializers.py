from rest_framework import serializers
from apps.serializer_extensions.serializers import PermissionRequiredInputField


class DisabledFieldCreateInputSerializerMixin(metaclass=serializers.SerializerMetaclass):
    is_disabled = PermissionRequiredInputField(
        permission="scouts_auth.access_disabled_entities", field=serializers.BooleanField(default=False)
    )


class DisabledFieldUpdateInputSerializerMixin(metaclass=serializers.SerializerMetaclass):
    is_disabled = PermissionRequiredInputField(
        permission="scouts_auth.access_disabled_entities",
        field=serializers.BooleanField(required=False),
        required=False,
    )
